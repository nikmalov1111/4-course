import csv
import os.path
import stream_encryption
import encrypt_aes
import metrics
from src import SHAChecker, PNGParser, key_sensitivity, MetaHandler

meta_path = input()

if os.path.isfile(meta_path):
    meta =  MetaHandler.MetaHandler(meta_path)
else:
    meta = MetaHandler.MetaHandler("metadata/meta.json")

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


if meta.action == "encrypt":
    print(f"\nШифрование по методу: {meta.algorithm}")
    match meta.algorithm:
        case "stream":
            stream_encryption.encrypt_decrypt_image(meta.source, meta.encrypted_path, meta.seed)
            stream_encryption.encrypt_decrypt_image(meta.encrypted_path, meta.decrypted_path, meta.seed)
        case "aes-ecb":
            salt: bytes
            if meta.salt != "null":
                salt = bytes.fromhex(meta.salt.strip())
                if len(salt) != 16:
                    raise Exception("невалидный nonce")

            else:
                salt = os.urandom(16)

            meta_path = encrypt_aes.encrypt_aes_ecb(meta.source, meta.encrypted_path, meta.secret_key, salt)
            encrypt_aes.decrypt_aes_ecb(meta.encrypted_path, meta.decrypted_path,  meta.secret_key, meta_path)
        case "aes-ctr":
            nonce: bytes
            if meta.nonce != "null":
                nonce = bytes.fromhex(meta.nonce.strip())
                if len(nonce) != 16:
                    raise Exception("невалидный nonce")
            else:
                nonce = os.urandom(16)

            salt: bytes
            if meta.salt != "null":
                salt = bytes.fromhex(meta.salt.strip())
                if len(salt) != 16:
                    raise Exception("невалидный nonce")

            else:
                salt = os.urandom(16)

            print(f"Используемый nonce: {nonce}")
            meta_path = encrypt_aes.encrypt_aes_ctr(meta.source, meta.encrypted_path, meta.secret_key, salt, nonce)
            encrypt_aes.decrypt_aes_ctr(meta.encrypted_path, meta.decrypted_path, meta.secret_key, meta_path)



    check_reversibility(meta.source, meta.decrypted_path)
    print_metrics(meta.algorithm, meta.source, meta.encrypted_path)
    key_sensitivity.key_sensitivity_test(meta.source, meta.algorithm)
    metrics.histogram(meta.source, meta.encrypted_path, histogram_path + meta.algorithm + "-histograms.png")

elif meta.action == "decrypt":
    print(f"\nДешифрование по методу: {meta.algorithm}")
    match meta.algorithm:
        case "stream":
            stream_encryption.encrypt_decrypt_image(meta.source, meta.decrypted_path, meta.seed)
        case "aes-ecb":
            encrypt_aes.decrypt_aes_ecb(meta.source, meta.decrypted_path, meta.secret_key, meta.meta_for_decrypt)
        case "aes-ctr":
            encrypt_aes.decrypt_aes_ctr(meta.source, meta.decrypted_path, meta.secret_key, meta.meta_for_decrypt)