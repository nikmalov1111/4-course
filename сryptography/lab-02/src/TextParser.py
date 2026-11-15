def text_to_bitstream(text: str):
    data = text.encode('utf-8')
    length = len(data)

    if length > 0xFFFFFFFF:
        raise ValueError("Текст слишком длинный")

    payload = length.to_bytes(4, byteorder='big') + data

    return ''.join(f'{byte:08b}' for byte in payload)


def bitstream_to_text(bitstream: str):
    if len(bitstream) % 8 != 0:
        raise ValueError("Длина битового потока должна быть кратна 8")
    if len(bitstream) < 32:
        raise ValueError("Битовый поток слишком короткий")

    data = bytes(
        int(bitstream[i:i + 8], 2)
        for i in range(0, len(bitstream), 8)
    )

    length = int.from_bytes(data[:4], byteorder='big')

    if len(data) - 4 < length:
        raise ValueError("Длина текста не совпадает с содержимым")

    text_bytes = data[4:4 + length]
    return text_bytes.decode('utf-8')

def bytes_to_bitstream(data: bytes):
    return ''.join(f'{byte:08b}' for byte in data)

def bitstream_to_bytes(bitstream: str):
    if len(bitstream) % 8 != 0:
        raise ValueError("Длина битового потока должна быть кратна 8")
    if len(bitstream) < 32:
        raise ValueError("Битовый поток слишком короткий")

    data = bytes(
        int(bitstream[i:i + 8], 2)
        for i in range(0, len(bitstream), 8)
    )

    length = int.from_bytes(data[:4], byteorder='big')

    if len(data) - 4 < length:
        raise ValueError("Длина байтов не совпадает с содержимым")

    return data[4:4 + length]