## Запуск программы
Запуск осуществляется через файл main.py. В начале программа потребует ввести путь к файлу meta.json. По умолчанию он находить в ../metadata/meta.json.
Пример структуры:
```json
{
  "algorithm": "p-lsb" | "e-lsb" | "er-lsb",
  "source": "your_path.png",
  "message": "your_message",
  "password": "your_password",
  "embedded_message_file": "your_path.png",
  "percent1": "0.01",
  "percent2": "0.05"
}
```
"algorithm", "source", "message", "password": имеют статус "required"
"embedded_message_file": "your_path.png" | "../images/embededMessageFiles/"+algorithm+"_stego_file_" + str(i) + ".png"
"percent1": "your_percent1" | "0.01"
"percent2": "your_percent2" | "0.05"
