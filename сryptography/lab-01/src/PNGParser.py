import os
import struct
import zlib
from typing import List, Tuple

class PNGParser:
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

    def __init__(self, file_path: str):
        if os.path.isfile(file_path):
            self.file_path = file_path
            self.header_chunks: List[Tuple[bytes, bytes]] = []
            self.footer_chunks: List[Tuple[bytes, bytes]] = []
            self._raw_data: bytes = b""

            self._load_and_parse()
        else:
            raise FileNotFoundError(f"Файл по пути {file_path} не найден")
    def get_ihdr_data(self):
        for chunk_type, chunk_data in self.header_chunks:
            if chunk_type == b'IHDR':
                return chunk_data
        raise ValueError("Отсутствует IHDR в файле.")

    def get_width(self):
        ihdr_data = self.get_ihdr_data()
        width = struct.unpack('>I', ihdr_data[0:4])[0]
        return width

    def get_height(self):
        ihdr_data = self.get_ihdr_data()
        height = struct.unpack('>I', ihdr_data[4:8])[0]
        return height



    def _load_and_parse(self):
        idat_contents = []
        passed_idat = False

        with open(self.file_path, 'rb') as f:
            if f.read(8) != self.PNG_SIGNATURE:
                raise ValueError("Не валидный.")

            while True:
                len_bytes = f.read(4)
                if not len_bytes:
                    break

                length = struct.unpack('>I', len_bytes)[0]
                chunk_type = f.read(4)
                chunk_data = f.read(length)
                f.seek(4, 1)

                if chunk_type == b'IDAT':
                    idat_contents.append(chunk_data)
                    passed_idat = True
                elif passed_idat:
                    self.footer_chunks.append((chunk_type, chunk_data))
                else:
                    self.header_chunks.append((chunk_type, chunk_data))

                if chunk_type == b'IEND':
                    break

        if not idat_contents:
            raise ValueError("Отсутствует IDAT в файле.")

        compressed_payload = b"".join(idat_contents)
        self._raw_data = zlib.decompress(compressed_payload)

    def get_raw_data(self):
        return self._raw_data

    def save(self, output_path: str, data: bytes):
        new_idat_payload = zlib.compress(data)
        with open(output_path, 'wb') as out:
            out.write(self.PNG_SIGNATURE)
            for c_type, c_data in self.header_chunks:
                self.write_chunk(out, c_type, c_data)
            self.write_chunk(out, b'IDAT', new_idat_payload)
            for c_type, c_data in self.footer_chunks:
                self.write_chunk(out, c_type, c_data)

    def write_chunk(self, file_object, chunk_type: bytes, chunk_data: bytes):
        file_object.write(struct.pack('>I', len(chunk_data)))
        file_object.write(chunk_type)
        file_object.write(chunk_data)
        crc = zlib.crc32(chunk_type + chunk_data) & 0xffffffff
        file_object.write(struct.pack('>I', crc))

    def get_image_info(self):
        ihdr = self.get_ihdr_data()
        width, height, bit_depth, color_type, _, _, _ = struct.unpack('>IIBBBBB', ihdr)
        if bit_depth != 8:
            raise ValueError(f"Поддерживается только глубина цвета 8 бит на канал. Глубина цвета: {bit_depth}")

        channels_map = {0: 1, 2: 3, 4: 2, 6: 4}
        if color_type not in channels_map:
            raise ValueError(f"Неподдерживаемый color_type: {color_type}")

        return width, height, channels_map[color_type]

    def get_pixels(self):
        width, height, bpp = self.get_image_info()
        stride = width * bpp
        raw = self._raw_data
        pixels = bytearray(height * stride)

        def paeth(a, b, c):
            p = a + b - c
            pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
            if pa <= pb and pa <= pc: return a
            if pb <= pc: return b
            return c

        pos = 0
        for y in range(height):
            filter_type = raw[pos]
            pos += 1
            row_start = y * stride

            for x in range(stride):
                val = raw[pos + x]
                a = pixels[row_start + x - bpp] if x >= bpp else 0
                b = pixels[row_start - stride + x] if y > 0 else 0
                c = pixels[row_start - stride + x - bpp] if (y > 0 and x >= bpp) else 0

                if filter_type == 0:
                    recon = val
                elif filter_type == 1:
                    recon = (val + a) & 0xff
                elif filter_type == 2:
                    recon = (val + b) & 0xff
                elif filter_type == 3:
                    recon = (val + ((a + b) >> 1)) & 0xff
                elif filter_type == 4:
                    recon = (val + paeth(a, b, c)) & 0xff
                else:
                    raise ValueError(f"Неизвестный фильтр PNG: {filter_type}")

                pixels[row_start + x] = recon
            pos += stride
        return pixels