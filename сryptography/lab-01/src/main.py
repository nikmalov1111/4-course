import csv
import json
import os.path
import stream_encryption
import encrypt_aes
import metrics
from src import SHAChecker, PNGParser, key_sensitivity

print("Путь к файлу meta.json:")
meta_path = input()
if meta_path == "":
    meta_path = "metadata/meta.json"

SECRET_SEED = 1234567890
SECRET_KEY = os.urandom(32)

default_png_encrypted_path = "../images/encrypted/"
default_png_decrypted_path = "../images/decrypted/"
metrics_path = "../results/"
histogram_path = "../results/"

def check_reversibility(source_path, decrypted_path):
    print("\nПроверка обратимости:")
    png_source = PNGParser.PNGParser(source_path)
    png_decrypted = PNGParser.PNGParser(decrypted_path)
    checker = SHAChecker.SHAChecker(png_source.get_raw_data(), png_decrypted.get_raw_data())

    print(f"Исходник:        {checker.get_hash1()}")
    print(f"Восстановленный: {checker.get_hash2()}")

    if checker.compare_bytes_sha256():
        print("Изображения совпадают по SHA256")
    else:
        print("Изображения НЕ совпадают по SHA256")


def print_metrics(algorithm, source_path, encrypted_path):
    print("\nМетрики:")
    metrics_of_source = metrics.test_image(source_path)
    entropy_of_source = metrics_of_source["entropy"]
    pixel_correlation_of_source = metrics_of_source["pixel_correlation"]

    metrics_of_encrypted = metrics.test_image(encrypted_path)
    entropy_of_encrypted = metrics_of_encrypted["entropy"]
    pixel_correlation_of_encrypted = metrics_of_encrypted["pixel_correlation"]

    data = [
        ["Метод", "Энтропия", "Сorr_H", "Сorr_V"],
        ["Исходное", entropy_of_source, pixel_correlation_of_source[0], pixel_correlation_of_source[1]],
        [algorithm, entropy_of_encrypted, pixel_correlation_of_encrypted[0], pixel_correlation_of_encrypted[1]]
    ]
    for row in data:
        print(f"{row[0]:<25} | {row[1]:<25} | {row[2]:<25} | {row[3]:<25}")

    with open(metrics_path+algorithm+".csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Результаты метрик сохранены в {metrics_path+algorithm+".csv"}")







if os.path.isfile(meta_path):
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    if ("algorithm" in meta) and ("source" in meta):
        encrypted_path = default_png_encrypted_path + meta["algorithm"] +"_png_encrypted.png"
        decrypted_path = default_png_decrypted_path + meta["algorithm"] +"_png_decrypted.png"
        if ("encrypted_path" in meta) and (meta["encrypted_path"] != "null"):
            encrypted_path = meta["encrypted_path"]
        if ("decrypted_path" in meta) and (meta["decrypted_path"] != "null"):
            decrypted_path = meta["decrypted_path"]

        if os.path.isfile(meta["source"]):
            if ("algorithm" in meta) and (meta["algorithm"] in ("stream", "aes_ctr", "aes_ecb")):
                match meta["algorithm"]:
                    case "stream":
                        print(f"\nШифрование по методу: {meta['algorithm']}")
                        stream_encryption.encrypt_decrypt_image(meta["source"],encrypted_path,SECRET_SEED)
                        stream_encryption.encrypt_decrypt_image(encrypted_path,decrypted_path,SECRET_SEED)
                    case "aes-ecb":
                        print(f"\nШифрование по методу: {meta['algorithm']}")
                        encrypt_aes.encrypt_aes_ecb(meta["source"], encrypted_path, SECRET_KEY)
                        encrypt_aes.decrypt_aes_ecb(encrypted_path, decrypted_path, SECRET_KEY)
                    case "aes-ctr":
                        print(f"\nШифрование по методу: {meta['algorithm']}")
                        if meta["nonce"] != "null":
                            encrypt_aes.encrypt_aes_ctr(meta["source"], encrypted_path, SECRET_KEY, meta["nonce"])
                        else:
                            encrypt_aes.encrypt_aes_ctr(meta["source"], encrypted_path, SECRET_KEY)
                        encrypt_aes.decrypt_aes_ctr(encrypted_path, decrypted_path, SECRET_KEY)

                check_reversibility(meta["source"], decrypted_path)
                print_metrics(meta["algorithm"], meta["source"], encrypted_path)
                key_sensitivity.key_sensitivity_test(meta["source"], meta["algorithm"])
                metrics.histogram(meta["source"], encrypted_path, histogram_path + meta['algorithm'] + "-histograms.png")
            else:
                print(f"В файле {meta_path} отсутствует или неверно поле algorithm")
        else:
            raise FileNotFoundError(f"Файл {meta["source"]} не найден")
    else:
        print(f"Отсутствуют требуемые поля в {meta_path}")
else:
    raise FileNotFoundError(f"Файл {meta_path} с метаданными не найден")
