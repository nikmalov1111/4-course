from TextParser import bitstream_to_text, text_to_bitstream
from PNGParser import PNGParser

def embed_message_in_pixels(pixels, message: str):
    pixels = list(pixels)
    bitstream = text_to_bitstream(message)

    if len(bitstream) > len(pixels):
        raise ValueError(
            f"Сообщение не помещается: нужно {len(bitstream)} бит, "
            f"доступно {len(pixels)} бит (макс. {len(pixels) // 8 - 4} байт)"
        )

    for i, bit in enumerate(bitstream):
        pixels[i] = (pixels[i] & 0xFE) | int(bit)
    return pixels

def extract_bits_of_message_from_pixels(pixels):
    pixels = list(pixels)

    if len(pixels) < 32:
        raise ValueError("Слишком мало данных")

    header = ''.join(str(pixels[i] & 1) for i in range(32))
    length = int(header, 2)

    total_bits = 32 + length * 8
    if total_bits > len(pixels):
        raise ValueError("В изображении нет корректного сообщения")

    bitstream = ''.join(str(pixels[i] & 1) for i in range(total_bits))
    return bitstream

def extract_message_from_pixels(pixels):
    bitstream = extract_bits_of_message_from_pixels(pixels)
    return bitstream_to_text(bitstream)

def embed_message_in_png(input_path: str, output_path: str, message: str):
    parser = PNGParser(input_path)
    pixels = parser.get_pixels()
    mode_pixels = embed_message_in_pixels(pixels, message)
    parser.save_as_png_with_new_pixels(output_path, mode_pixels)

def extract_message_from_png(input_path: str):
    parser = PNGParser(input_path)
    mode_pixels = parser.get_pixels()
    return extract_message_from_pixels(mode_pixels)
