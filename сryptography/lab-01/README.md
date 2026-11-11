# Запуск программы
Запуск осуществляется через файл `main.py`. При запуске программа потребует ввести путь к файлу `meta.json` с параметрами запуска.
Структура файла предполагает обязательное наличие полей `"algorithm"` (метод шифрования: `"stream" | "aes-ecb" | "aes-ctr"`) и `"source"` ( `.png` , путь к файлу, который нужно зашифровать).
Также есть необязательные поля: `"nonce"` (для метода `aes-ctr`), `"decrypted_path"` ( `*.png` , путь к файлу, где будет находиться зашифрованное изображение) и
`"encrypted_path"` ( `.png` , аналогично `"decryption_path"`, только восстановленное изображение).
Дефолтный файл `meta.json` лежит по пути `../src/metadata/meta.json`
Пример структуры файла `meta.json`.
```json
{
  "algorithm": "stream | aes-ecb | aes-ctr",
  "nonce": "your_nonce | null", 
  "source": "../images/tu-tu-du-du.png | your_source_path.png",
  "decrypted_path": "your_decrypted_path.png | null",
  "encrypted_path": "your_encrypted_path.png | null"
}
```
