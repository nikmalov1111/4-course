import csv
import os.path
import PlainLSB
import EncryptedLSB
import EncryptedRandomLSB
from MetaHandler import MetaHandler
import Metrics

def print_introduction(meta: MetaHandler):
    print(f"Встраивание сообщения по методу {meta.algorithm}.\n")
    print(f"Сообщение: {meta.message}\n")
    print(f"Путь к исходному изображению: {meta.source}\n")
    print(f"Путь к обработанному изображению: {meta.embedded_message_file}\n")
    print(f"Проценты объема текста для теста чувствительности: {float(meta.percent1) * 100}% и {float(meta.percent2) * 100}%. Текст генерируется автоматически.\n")
    print("Обработка...")

def calculate_test_metrics(meta: MetaHandler, received_message: str):
    Metrics.matching_test(meta.message, received_message)
    psnr_val, ssim_val = Metrics.calculate_psnr_and_ssim(meta.source, meta.embedded_message_file)
    changed_count, changed_ratio = Metrics.calculate_changed_ratio(meta.source, meta.embedded_message_file)
    p_zero_cover, p_one_cover = Metrics.calculate_lsb_distribution(meta.source)
    p_zero_stego, p_one_stego = Metrics.calculate_lsb_distribution(meta.embedded_message_file)
    chi2_cover, p_value_cover = Metrics.chi_square_test(meta.source)
    chi2_stego, p_value_stego = Metrics.chi_square_test(meta.embedded_message_file)

    print("\nРезультаты PSNR, SSIM, Changed Ratio:")
    print(f"{'Вариант':<25} | {'PSNR (дБ)':<25} | {'SSIM':<25} | {'changed_ratio':<25}")
    print("-" * 80)
    print(f"{meta.algorithm:<25} | {psnr_val:<25} | {ssim_val:<25} | {changed_ratio:<25}")

    print("\nРезультаты распределение LSB, χ²-анализ:")
    print(f"{'Вариант':<25} | {'P(LSB=0)':<25} | {'P(LSB=1)':<25} | {'χ²':<25} | {'p-value':<25}")
    print("-" * 80)
    print(f"{"cover":<25} | {p_zero_cover:<25} | {p_one_cover:<25} | {chi2_cover:<25} | {p_value_cover:<15.15e}")
    print(f"{meta.algorithm:<25} | {p_zero_stego:<25} | {p_one_stego:<25} | {chi2_stego:<25} | {p_value_stego:<15.15e}\n")

    Metrics.create_difference_map(meta.algorithm, meta.source, meta.embedded_message_file)
    Metrics.save_comparative_histogram(meta.algorithm, meta.source, meta.embedded_message_file)

    data = [
        ["Вариант", "PSNR", "SSIM", "Changed ratio", "P(LSB=1)", "χ²", "p-value"],
        [meta.algorithm, psnr_val, ssim_val, changed_ratio, p_one_stego, chi2_stego, p_value_stego]
    ]

    metrics_path = "../results/" + meta.algorithm + "_metrics_"
    i = 1
    while os.path.isfile(metrics_path + str(i) + ".csv"):
        i+=1
    metrics_path = metrics_path + str(i) + ".csv"

    with open(metrics_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Метрики сохранены в {metrics_path}")

    Metrics.data_volume_sensitivity_test(meta)

meta_path = input()
if meta_path == "":
    meta_path = "../metadata/meta.json"

meta = MetaHandler(meta_path)
print_introduction(meta)
new_message = ""

match meta.algorithm:
    case "p-lsb":
        PlainLSB.embed_message_in_png(meta.source, meta.embedded_message_file, meta.message)
        new_message = PlainLSB.extract_message_from_png(meta.embedded_message_file)
    case "e-lsb":
        EncryptedLSB.embed_message_in_png(meta.source, meta.embedded_message_file, meta.message, meta.password)
        new_message = EncryptedLSB.extract_message_from_png(meta.embedded_message_file, meta.password)
    case "er-lsb":
        EncryptedRandomLSB.embed_message_in_png(meta.source, meta.embedded_message_file, meta.message, meta.password)
        new_message = EncryptedRandomLSB.extract_message_from_png(meta.embedded_message_file, meta.password)
calculate_test_metrics(meta, new_message)
