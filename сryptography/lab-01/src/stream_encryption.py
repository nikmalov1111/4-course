import os.path
from PNGParser import PNGParser

class Xorshift32:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 1

    def next_byte(self):
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x
        return x & 0xFF

def encrypt_decrypt_image(input_file, output_file, seed):
    if os.path.isfile(input_file):
        parser = PNGParser(input_file)
        data = parser.get_raw_data()

        xorshift = Xorshift32(seed)

        result = bytearray(len(data))
        for i in range(len(data)):
            keystream_byte = xorshift.next_byte()
            result[i] = data[i] ^ keystream_byte

        parser.save(output_file, result)

        print(f"Файл успешно обработан потоковым шифрованием и сохранен как: {output_file}")
    else:
        raise FileNotFoundError(f"Файл по пути {input_file} не найден")