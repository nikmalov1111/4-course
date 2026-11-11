import math
import os
from collections import Counter
from matplotlib import pyplot as plt
from src.PNGParser import PNGParser


def calculate_entropy(data: bytes):
    if not data:
        return 0.0
    counts = Counter(data)
    total_bytes = len(data)

    entropy = 0.0
    for count in counts.values():
        p = count / total_bytes
        entropy -= p * math.log2(p)

    return entropy


def calculate_pearson_correlation(x: list, y: list):
    n = len(x)
    if n <= 1:
        return 0.0

    sum_x = sum(x)
    sum_y = sum(y)
    mean_x = sum_x / n
    mean_y = sum_y / n

    compositions = 0
    sum_dx2 = 0
    sum_dy2 = 0
    for xi, yi in zip(x, y):
        dx = xi - mean_x
        dy = yi - mean_y
        compositions += dx * dy
        sum_dx2 += dx**2
        sum_dy2 += dy**2

    if sum_dx2 == 0 or sum_dy2 == 0:
        return 0.0

    return compositions / math.sqrt(sum_dx2 * sum_dy2)

def calculate_pixel_correlation(data: bytes, width: int, height: int):
    matrix = [list(data[i * width : (i + 1) * width]) for i in range(height)]

    x_hor, y_hor = [], []
    for y in range(height):
        for x in range(width - 1):
            x_hor.append(matrix[y][x])
            y_hor.append(matrix[y][x + 1])

    x_ver, y_ver = [], []
    for y in range(height - 1):
        for x in range(width):
            x_ver.append(matrix[y][x])
            y_ver.append(matrix[y + 1][x])

    corr_h = calculate_pearson_correlation(x_hor, y_hor)
    corr_v = calculate_pearson_correlation(x_ver, y_ver)

    return corr_h, corr_v

def test_image(image_path: str):
    if os.path.isfile(image_path):
        parser = PNGParser(image_path)
        data = parser.get_raw_data()
        entropy = calculate_entropy(data)
        pixel_correlation = calculate_pixel_correlation(data, parser.get_width(), parser.get_height())
        return dict(entropy=entropy, pixel_correlation=pixel_correlation)
    else:
        raise FileNotFoundError(f"Файл по пути {image_path} не найден")

def count_values(byte_data: bytes | bytearray):
    total = len(byte_data)
    counts = [0] * 256
    for val in byte_data:
        counts[val] += 1
    return [c * 100 / total for c in counts]


def histogram(input_file1: str, input_file2: str, output_path: str):
    if os.path.isfile(input_file1) and os.path.isfile(input_file2):
        parser1 = PNGParser(input_file1)
        pixels1 = parser1.get_pixels()

        parser2 = PNGParser(input_file2)
        pixels2 = parser2.get_raw_data()

        counts1 = count_values(pixels1)
        counts2 = count_values(pixels2)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.bar(range(256), counts1, width=1.0, color='steelblue', edgecolor='black', linewidth=0.2)
        ax1.set_title(input_file1)
        ax1.set_xlabel("Значение пикселя (0–255)")
        ax1.set_ylabel("Частота, %")
        ax1.set_xlim(0, 255)
        ax1.grid(axis='y', alpha=0.3)

        ax2.bar(range(256), counts2, width=1.0, color='darkorange', edgecolor='black', linewidth=0.2)
        ax2.set_title(input_file2)
        ax2.set_xlabel("Значение пикселя (0–255)")
        ax2.set_ylabel("Частота, %")
        ax2.set_xlim(0, 255)
        ax2.grid(axis='y', alpha=0.3)
        plt.tight_layout()


        plt.savefig(output_path, format='png', bbox_inches='tight', dpi=300)
        plt.close()

        print(f"\nГистограмма частот значений пикселей сохранена как: {output_path}")
    else:
        raise FileNotFoundError(f"Файл {input_file1} или файл {input_file2} не найден")