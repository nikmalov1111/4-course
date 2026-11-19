import json
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import PNGParser

def derive_key(secret: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(secret.encode('utf-8'))

def encrypt_aes_ecb(input_file, output_file, secret, salt):
    meta_path_ecb = ""
    key = derive_key(secret, salt)

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
            "source": input_file,
            "padding": ciphertext[original_len:].hex(),
            "original_len": original_len,
            "salt": base64.b64encode(salt).decode('utf-8')
        }

        meta_path_ecb = "metadata/meta_ecb/meta_ecb"
        i = 1
        while os.path.isfile(f"{meta_path_ecb}({i}).json"):
            i += 1
        meta_path_ecb = f"{meta_path_ecb}({i}).json"

        with open(meta_path_ecb, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=4)

        print(f"Файл зашифрован алгоритмом AES_ECB и сохранен как: {output_file}, метаданные шифрования сохранены как {meta_path_ecb}")
    else:
        print(f"Файла {input_file} не существует!")

    return meta_path_ecb

def decrypt_aes_ecb(input_file, output_file, secret, meta_path_ecb):
    if os.path.isfile(meta_path_ecb):
        if os.path.isfile(input_file):
            with open(meta_path_ecb, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            original_len = meta["original_len"]
            padding_data = bytes.fromhex(meta["padding"])
            salt = base64.b64decode(meta["salt"])
            key = derive_key(secret, salt)

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


def encrypt_aes_ctr(input_file, output_file, secret, salt, nonce):
    meta_path_ctr = ""
    if os.path.isfile(input_file):

        key = derive_key(secret, salt)

        parser = PNGParser.PNGParser(input_file)
        data = parser.get_raw_data()
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        meta = {
            "source": input_file,
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "salt": base64.b64encode(salt).decode('utf-8')
        }

        meta_path_ctr = "metadata/meta_ctr/meta_ctr"
        i = 1
        while os.path.isfile(f"{meta_path_ctr}({i}).json"):
            i += 1
        meta_path_ctr = f"{meta_path_ctr}({i}).json"

        with open(meta_path_ctr, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=4)

        parser.save(output_file, ciphertext)

        print(f"Файл зашифрован алгоритмом AES_CTR и сохранен как: {output_file}, метаданные шифрования сохранены как {meta_path_ctr}")
    else:
        print(f"Файла {input_file} не существует!")

    return meta_path_ctr

def decrypt_aes_ctr(input_file, output_file, secret, meta_path_ctr):
    if os.path.isfile(meta_path_ctr):
        with open(meta_path_ctr, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        if os.path.isfile(input_file):

            nonce = base64.b64decode(meta["nonce"])
            salt = base64.b64decode(meta["salt"])

            key = derive_key(secret, salt)
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
        print(f"Метаданные {meta_path_ctr} отсутствуют!")




def encrypt_aes_ecb_for_test(input_file, output_file, key):

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

        print(f"Файл зашифрован алгоритмом AES_ECB и сохранен как: {output_file}")
    else:
        print(f"Файла {input_file} не существует!")



def encrypt_aes_ctr_for_test(input_file, output_file, key, nonce):
    if os.path.isfile(input_file):
        parser = PNGParser.PNGParser(input_file)
        data = parser.get_raw_data()
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        parser.save(output_file, ciphertext)

        print(f"Файл зашифрован алгоритмом AES_CTR и сохранен как: {output_file}")
    else:
        print(f"Файла {input_file} не существует!")