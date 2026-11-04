MAC Address DB

Парсер логов сетевого оборудования в SQLite + CLI-поиск по MAC-адресам.

Usage

Загрузка данных:
# Положите .txt файлы в текущую директорию
python parser.py

Поиск:
./search_mac.sh
Enter MAC (like askg4h2g): a1b2c3


Requirements

- Python 3.6+
- `sqlite3` (CLI)

Notes

- Входные файлы: `*.txt` с датой в имени (`_ДД-ММ`)
- Повторный запуск не дублирует данные, только дополняет
- Хранятся до 10 последних дат появления MAC
