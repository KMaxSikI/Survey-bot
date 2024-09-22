import json
from pathlib import Path

# Определяем путь к файлу с данными пользователей
USER_DATA_FILE = Path(__file__).parent.parent.parent / "db" / "users.json"


# Функция для сохранения данных пользователей в JSON-файл
def save_users_to_json(users):
    # Открываем файл для записи, устанавливаем кодировку UTF-8
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        # Записываем данные пользователей в формате JSON
        json.dump(users, file, ensure_ascii=False, indent=4)


# Функция для загрузки данных пользователей из JSON-файла
def load_users_from_json():
    try:
        # Открываем файл для чтения, устанавливаем кодировку UTF-8
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            # Загружаем и возвращаем данные из JSON-файла
            return json.load(file)
    except FileNotFoundError:
        # Если файл не найден, возвращаем пустой словарь
        return {}
