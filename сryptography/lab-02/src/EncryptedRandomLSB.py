import hashlib
import os
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PNGParser import PNGParser
from TextParser import bytes_to_bitstream, bitstream_to_bytes

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

def get_shuffled_indices(count_pixels: int, password: str):
    seed_bytes = hashlib.sha256(password.encode('utf-8')).digest()
    seed_int = int.from_bytes(seed_bytes[:4], 'big')
    rng = random.Random(seed_int)
    indices = list(range(count_pixels))
    rng.shuffle(indices)
    return indices

def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode('utf-8'))


def encrypt_message(text: str, password: str):
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = derive_key(password, salt)
    aes_gcm = AESGCM(key)

    ciphertext = aes_gcm.encrypt(nonce, text.encode('utf-8'), None)

    length_payload = len(ciphertext) + SALT_SIZE + NONCE_SIZE

    if length_payload > 0xFFFFFFFF:
        raise ValueError("payload слишком длинный")

    payload = length_payload.to_bytes(4, 'big') + salt + nonce + ciphertext
    return payload

def encrypt_message_with_nonce_and_salt(text: str, password: str, nonce: bytes, salt: bytes):  #для теста
    if (len(nonce) != NONCE_SIZE) or (len(salt) != SALT_SIZE):
        raise ValueError("nonce или salt невалидные")

    key = derive_key(password, salt)
    aes_gcm = AESGCM(key)

    ciphertext = aes_gcm.encrypt(nonce, text.encode('utf-8'), None)

    length_payload = len(ciphertext) + SALT_SIZE + NONCE_SIZE

    if length_payload > 0xFFFFFFFF:
        raise ValueError("payload слишком длинный")

    payload = length_payload.to_bytes(4, 'big') + salt + nonce + ciphertext
    return payload

def decrypt_message(payload: bytes, password: str):
    if len(payload) < SALT_SIZE + NONCE_SIZE:
        raise ValueError("payload слишком короткий")

    salt = payload[:SALT_SIZE]
    nonce = payload[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = payload[SALT_SIZE + NONCE_SIZE:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception:
        raise ValueError("Неверный пароль или данные повреждены!")


def embed_payload_in_pixels(pixels, indices, payload: bytes):
    pixels = list(pixels)
    bitstream = bytes_to_bitstream(payload)

    if len(bitstream) > len(pixels):
        raise ValueError(
            f"Сообщение не помещается: нужно {len(bitstream)} бит, "
            f"доступно {len(pixels)} бит (макс. {len(pixels) // 8 - 4} байт)"
        )

    for i in range(len(bitstream)):
        bit = bitstream[i]
        index = indices[i]
        pixels[index] = (pixels[index] & 0xFE) | int(bit)

    return pixels

def extract_bits_of_payload_from_pixels(pixels, indices):
    pixels = list(pixels)

    if len(pixels) < 32:
        raise ValueError("Слишком мало данных")

    header = ''.join(str(pixels[indices[i]] & 1) for i in range(32))
    length = int(header, 2)

    total_bits = 32 + length * 8
    if total_bits > len(pixels):
        raise ValueError("В изображении нет корректного сообщения")

    bitstream = ''.join(str(pixels[indices[i]] & 1) for i in range(total_bits))
    return bitstream

def extract_payload_from_pixels(pixels, indices):
    bitstream = extract_bits_of_payload_from_pixels(pixels, indices)
    return bitstream_to_bytes(bitstream)

def embed_message_in_png(input_path: str, output_path: str, message: str, password: str):
    parser = PNGParser(input_path)
    pixels = parser.get_pixels()
    indices = get_shuffled_indices(len(pixels), password)
    mode_pixels = embed_payload_in_pixels(pixels, indices, encrypt_message(message, password))
    parser.save_as_png_with_new_pixels(output_path, mode_pixels)

def extract_message_from_png(input_path: str, password: str):
    parser = PNGParser(input_path)
    mode_pixels = parser.get_pixels()
    indices = get_shuffled_indices(len(mode_pixels), password)
    payload = extract_payload_from_pixels(mode_pixels, indices)
    return decrypt_message(payload, password)

def embed_message_in_png_with_nonce_and_salt(input_path: str, output_path: str, message: str, password: str, nonce: bytes, salt: bytes):   #для теста
    parser = PNGParser(input_path)
    pixels = parser.get_pixels()
    indices = get_shuffled_indices(len(pixels), password)
    mode_pixels = embed_payload_in_pixels(pixels, indices, encrypt_message_with_nonce_and_salt(message, password, nonce, salt))
    parser.save_as_png_with_new_pixels(output_path, mode_pixels)