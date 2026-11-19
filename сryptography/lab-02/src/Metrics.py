import os
import random
import string
import numpy as np
import plt
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from scipy import stats
from PNGParser import PNGParser
import EncryptedRandomLSB
import PlainLSB
import EncryptedLSB
from MetaHandler import MetaHandler

def matching_test(text1:str, text2:str):
    if text1 == text2:
        print("Сообщения совпали!")
    else:
        print("Сообщения НЕ совпали!")

def calculate_psnr_and_ssim(original_path: str, stego_path: str):
    parser_orig = PNGParser(original_path)
    parser_stego = PNGParser(stego_path)

    width = parser_orig.get_width()
    height = parser_orig.get_height()
    planes = parser_orig.meta.get('planes', 3)
    
    img_orig = np.array(parser_orig.get_pixels(), dtype=np.float64).reshape((height, width, planes))
    img_stego = np.array(parser_stego.get_pixels(), dtype=np.float64).reshape((height, width, planes))

    
    if img_orig.shape != img_stego.shape:
        raise ValueError("размеры изображений не совпадают")

    psnr_val = peak_signal_noise_ratio(img_orig, img_stego, data_range=255)
    ssim_val = structural_similarity(img_orig, img_stego, data_range=255, channel_axis=-1)

    return psnr_val, ssim_val


def calculate_changed_ratio(original_path: str, stego_path: str):
    parser_orig = PNGParser(original_path)
    parser_stego = PNGParser(stego_path)
    orig_pixels = parser_orig.get_pixels()
    stego_pixels = parser_stego.get_pixels()

    if len(orig_pixels) != len(stego_pixels):
        raise ValueError("размеры изображений не совпадают")

    total_components = len(orig_pixels)

    changed_count = sum(1 for a, b in zip(orig_pixels, stego_pixels) if a != b)
    changed_ratio = (changed_count / total_components) * 100

    return changed_count, changed_ratio


def calculate_lsb_distribution(image_path: str):
    parser = PNGParser(image_path)
    pixels = parser.get_pixels()
    total = len(pixels)
    count_zeros = 0
    count_ones = 0

    for byte in pixels:
        if (byte & 1) == 0:
            count_zeros += 1
        else:
            count_ones += 1

    p_zero = count_zeros / total
    p_one = count_ones / total

    return p_zero, p_one

def chi_square_test(image_path: str):
    parser = PNGParser(image_path)
    pixels = np.array(parser.pixels)
    counts, _ = np.histogram(pixels, bins=256, range=(0, 256))
    f_obs = []
    f_exp = []

    for k in range(128):
        n_2k = counts[2 * k]
        n_2k1 = counts[2 * k + 1]
        expected = (n_2k + n_2k1) / 2.0
        f_obs.extend([n_2k, n_2k1])
        f_exp.extend([expected, expected])
    f_obs = np.array(f_obs)
    f_exp = np.array(f_exp)
    chi2, p_value = stats.chisquare(f_obs, f_exp)

    return chi2, p_value

def calculate_metrics(original_path, stego_path):
    psnr_val, ssim_val = calculate_psnr_and_ssim(original_path, stego_path)
    changed_count, changed_ratio = calculate_changed_ratio(original_path, stego_path)
    chi2, p_value = chi_square_test(stego_path)
    return psnr_val, ssim_val, changed_ratio, p_value

def create_difference_map(algorithm: str, cover_path: str, stego_path: str):
    parser_cover = PNGParser(cover_path)
    parser_stego = PNGParser(stego_path)
    cover_pixels = np.array(parser_cover.get_pixels(), dtype=np.int16)
    stego_pixels = np.array(parser_stego.get_pixels(), dtype=np.int16)

    diff = np.abs(cover_pixels - stego_pixels)
    diff_amplified = diff * 255

    diff_pixels = np.clip(diff_amplified, 0, 255).astype(np.uint8).tolist()

    planes = parser_cover.meta.get('planes', 3)
    has_alpha = parser_cover.meta.get('alpha', False)

    if has_alpha and planes == 4:
        for i in range(3, len(diff_pixels), 4):
            diff_pixels[i] = 255

    output_path = "../results/"+ algorithm +"_difference_map_"
    i = 1
    while os.path.isfile(output_path + str(i) + ".png"):
        i+=1
    output_path = output_path+str(i)+".png"

    parser_cover.save_as_png_with_new_pixels(output_path, diff_pixels)
    print(f"Карта разности сохранена в {output_path}")

def save_comparative_histogram(algorithm: str, cover_path: str, stego_path: str):
    parser_cover = PNGParser(cover_path)
    parser_stego = PNGParser(stego_path)
    cover_pixels = np.array(parser_cover.get_pixels())
    stego_pixels = np.array(parser_stego.get_pixels())

    plt.figure(figsize=(12, 6))
    plt.hist(cover_pixels, bins=256, range=(0, 256), histtype='step', label='Cover (исходное)', color='blue', linewidth=1.5)
    plt.hist(stego_pixels, bins=256, range=(0, 256), histtype='step', label='Stego (сообщение)', color='red', linewidth=1.5, linestyle='--')
    plt.title('Сравнительная гистограмма значений пикселей')
    plt.xlabel('Значение пикселя (0-255)')
    plt.ylabel('Количество пикселей')
    plt.legend(loc='upper right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    output_path = "../results/"+ algorithm +"_histogram_"
    i = 1
    while os.path.isfile(output_path + str(i) + ".png"):
        i += 1
    output_path = output_path + str(i) + ".png"

    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Гистограмма успешно сохранена в файл: {output_path}")


def data_volume_sensitivity_test(meta: MetaHandler):
    percent1 = float(meta.percent1)
    percent2 = float(meta.percent2)
    input_file = meta.source
    algorithm = meta.algorithm

    if (percent1 > 1) or (percent1 < 0) or (percent2 > 1) or (percent2 < 0):
        raise ValueError("невалидные проценты")

    output_file_1 = "../images/stego_1.png"
    output_file_2 = "../images/stego_2.png"

    print("\nТест чувствительности к объему данных. Текст генерируется автоматический")
    parser = PNGParser(input_file)
    capacity_bits = len(parser.pixels)
    max_text_bytes = (capacity_bits // 8) - 50
    print(f"Путь к файлу stego_1: {output_file_1}")
    print(f"Путь к файлу stego_2: {output_file_2}")

    print(f"Максимальная ёмкость для текста: ~{max_text_bytes} байт\n")

    characters = string.ascii_letters + string.digits

    text_1 = ''.join(random.choice(characters) for _ in range(int(max_text_bytes * percent1)))
    text_2 = ''.join(random.choice(characters) for _ in range(int(max_text_bytes * percent2)))

    match algorithm:
        case "p-lsb":
            print("Тестируем на алгоритме PlainLSB")
            PlainLSB.embed_message_in_png(input_file, output_file_1, text_1)
            PlainLSB.embed_message_in_png(input_file, output_file_2, text_2)
            psnr_val1, ssim_val1, changed_ratio1, p_value1 = calculate_metrics(input_file, output_file_1)
            psnr_val2, ssim_val2, changed_ratio2, p_value2 = calculate_metrics(input_file, output_file_2)
            if (PlainLSB.extract_message_from_png(output_file_1) != text_1) or (
                    PlainLSB.extract_message_from_png(output_file_2) != text_2):
                raise ValueError("данные НЕ сошлись")

        case "e-lsb":
            password = meta.password
            print("Тестируем на алгоритме EncryptedLSB")
            EncryptedLSB.embed_message_in_png(input_file, output_file_1, text_1, password)
            EncryptedLSB.embed_message_in_png(input_file, output_file_2, text_2, password)
            psnr_val1, ssim_val1, changed_ratio1, p_value1 = calculate_metrics(input_file, output_file_1)
            psnr_val2, ssim_val2, changed_ratio2, p_value2 = calculate_metrics(input_file, output_file_2)
            if (EncryptedLSB.extract_message_from_png(output_file_1, password) != text_1) or (EncryptedLSB.extract_message_from_png(output_file_2, password) != text_2):
                raise ValueError("данные НЕ сошлись")

        case "er-lsb":
            password = meta.password
            print("Тестируем на алгоритме EncryptedRandomLSB")
            EncryptedRandomLSB.embed_message_in_png(input_file, output_file_1, text_1, password)
            EncryptedRandomLSB.embed_message_in_png(input_file, output_file_2, text_2, password)
            psnr_val1, ssim_val1, changed_ratio1, p_value1 = calculate_metrics(input_file, output_file_1)
            psnr_val2, ssim_val2, changed_ratio2, p_value2 = calculate_metrics(input_file, output_file_2)
            if (EncryptedRandomLSB.extract_message_from_png(output_file_1, password) != text_1) or (EncryptedRandomLSB.extract_message_from_png(output_file_2, password) != text_2):
                raise ValueError("данные НЕ сошлись")

    print("\nРезультаты:")
    print(f"\n{'Заполнение':<15} | {'PSNR (дБ)':<10} | {'SSIM':<10} | {'changed_ratio':<15} | {'p-value':<15}")
    print("-" * 65)
    print(f"{str(float(percent1) * 100) + '% (~' + str(len(text_1)) + ' байт)':<15} | {psnr_val1:<15} | {ssim_val1:<15} | {changed_ratio1:<15} | {p_value1:<15.2e}")
    print(f"{str(float(percent2) * 100) + '% (~' + str(len(text_2)) + ' байт)':<15} | {psnr_val2:<15} | {ssim_val2:<15} | {changed_ratio2:<15} | {p_value2:<15.2e}")
