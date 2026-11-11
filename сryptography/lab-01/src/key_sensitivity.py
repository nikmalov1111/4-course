import os
import encrypt_aes
import stream_encryption
from PNGParser import PNGParser


def calculate_npcr_uaci(data1: bytes, data2: bytes):
    n = len(data1)
    diff_count = 0
    sum_abs_diff = 0

    for b1, b2 in zip(data1, data2):
        if b1 != b2:
            diff_count += 1
        sum_abs_diff += abs(b1 - b2)
    npcr = (diff_count / n) * 100.0
    uaci = (sum_abs_diff / (255.0 * n)) * 100.0

    return npcr, uaci


def key_sensitivity_test(source_image_path, algorithm):
    print(f"\nТест чувствительности к изменению ключа (метод: {algorithm})")

    out1 = "../images/encrypted/encrypted_k1.png"
    out2 = "../images/encrypted/encrypted_k2.png"

    if algorithm == "aes-ctr":
        key1 = os.urandom(32)
        key2 = bytearray(key1)
        key2[0] ^= 0x01
        key2 = bytes(key2)

        print(f"Ключ 1: {key1}")
        print(f"Ключ 2: {key2}")

        encrypt_aes.encrypt_aes_ctr(source_image_path, out1, key1)
        encrypt_aes.encrypt_aes_ctr(source_image_path, out2, key2)

    elif algorithm == "aes-ecb":
        key1 = os.urandom(32)
        key2 = bytearray(key1)
        key2[0] ^= 0x01
        key2 = bytes(key2)

        print(f"Ключ 1: {key1}")
        print(f"Ключ 2: {key2}")

        encrypt_aes.encrypt_aes_ecb(source_image_path, out1, key1)
        encrypt_aes.encrypt_aes_ecb(source_image_path, out2, key2)

    elif algorithm == "stream":
        seed1 = 1234567890
        seed2 = seed1 ^ 1

        print(f"Seed 1: {seed1}")
        print(f"Seed 2: {seed2}")

        stream_encryption.encrypt_decrypt_image(source_image_path, out1, seed1)
        stream_encryption.encrypt_decrypt_image(source_image_path, out2, seed2)
    else:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")

    parser1 = PNGParser(out1)
    parser2 = PNGParser(out2)

    data1 = parser1.get_raw_data()
    data2 = parser2.get_raw_data()

    npcr, uaci = calculate_npcr_uaci(data1, data2)

    print("Результаты теста")
    print(f"NPCR = {npcr:.4f}%")
    print(f"UACI = {uaci:.4f}%")

    return npcr, uaci