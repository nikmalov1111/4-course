import json
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import PNGParser

def encrypt_aes_ecb(input_file, output_file, key, meta_path_ecb="metadata/meta_ecb.json"):
    if os.path.isfile(input_file):

        parser = PNGParser.PNGParser(input_file)
        data = parser.get_raw_data()
        original_len = len(data)

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        parser.save(output_file, ciphertext[:original_len])

        meta = {
            "padding": ciphertext[original_len:].hex(),
            "original_len": original_len
        }

        with open(meta_path_ecb, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=4)

        print(f"Файл зашифрован алгоритмом AES_ECB и сохранен как: {output_file}")
    else:
        print(f"Файла {input_file} не существует!")

def decrypt_aes_ecb(input_file, output_file, key, meta_path_ecb="metadata/meta_ecb.json"):
    if os.path.isfile(meta_path_ecb):
        if os.path.isfile(input_file):
            with open(meta_path_ecb, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            original_len = meta["original_len"]
            padding_data = bytes.fromhex(meta["padding"])

            parser = PNGParser.PNGParser(input_file)
            ciphertext = parser.get_raw_data() + padding_data

            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            data = padded_data[:original_len]

            parser.save(output_file, data)

            print(f"Файл успешно расшифрован алгоритмом AES_ECB и сохранен как: {output_file}")
        else:
            print(f"Файла {input_file} не существует!")
    else:
        print(f"Метаданные {meta_path_ecb} отсутствуют!")


def encrypt_aes_ctr(input_file, output_file, key, nonce=os.urandom(16), meta_path_ctr="metadata/meta_ctr.json"):
    if os.path.isfile(input_file):
        parser = PNGParser.PNGParser(input_file)
        data = parser.get_raw_data()
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        meta = {
            "nonce": base64.b64encode(nonce).decode('utf-8')
        }

        with open(meta_path_ctr, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=4)

        parser.save(output_file, ciphertext)

        print(f"Файл зашифрован алгоритмом AES_CTR и сохранен как: {output_file}")
    else:
        print(f"Файла {input_file} не существует!")

def decrypt_aes_ctr(input_file, output_file, key, meta_path_ctr="metadata/meta_ctr.json"):
    if os.path.isfile(meta_path_ctr):
        with open(meta_path_ctr, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        nonce = base64.b64decode(meta["nonce"].encode('utf-8'))

        if os.path.isfile(input_file):
            parser = PNGParser.PNGParser(input_file)
            encrypted_data = parser.get_raw_data()

            cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            data = decryptor.update(encrypted_data) + decryptor.finalize()

            parser.save(output_file, data)

            print(f"Файл успешно расшифрован алгоритмом AES_CTR и сохранен как: {output_file}")
        else:
            print(f"Файла {input_file} не существует!")
    else:
        print(f"Отсутствуют метаданные по пути: {meta_path_ctr}")