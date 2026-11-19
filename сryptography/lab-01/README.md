# Запуск программы
Запуск осуществляется через файл `main.py`. При запуске программа потребует ввести путь к файлу `meta.json` с параметрами запуска.
Структура файла предполагает обязательное наличие полей `"algorithm"` (метод шифрования: `"stream" | "aes-ecb" | "aes-ctr"`), `"action"` (режим работы: `"encrypt | decrypt"`),  `"source"` ( `.png` , при режиме `"encrypt"` - путь к файлу, который нужно зашифровать, при режиме `"decrypt"` - путь к файлу, который нужно дешифровать), `"seed"` (required для алгоритма "stream"), `"secret_key"` (required для алгоритмов ecb и ctr), `"meta_for_decrypt"` (required для режима `"decrypt"`).
Также есть необязательные поля: `"nonce"` (для метода `aes-ctr` и режима шифрования), `"salt"` (для режима шифрования и алгоритмов ecb и ctr), `"decrypted_path"` ( `*.png` , путь к файлу, где будет находиться дешифрованное изображение) и
`"encrypted_path"` ( `.png` , аналогично `"decryption_path"`, только зашифрованное изображение).
Дефолтный файл `meta.json` лежит по пути `../src/metadata/meta.json`
Пример структуры файла `meta.json`.
```json
{
  "action": "encrypt",
  "algorithm": "aes-ctr",
  "source": "../images/tu-tu-du-du.png",
  "seed": "null",
  "secret_key": "12345",
  "nonce": "null",
  "salt": "null",
  "decrypted_path": "null",
  "encrypted_path": "null",
  "meta_for_decrypt": "null"
}
```
