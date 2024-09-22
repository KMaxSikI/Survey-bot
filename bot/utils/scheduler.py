from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Employee
from bot.utils.telegram_api import remove_user_from_group
import json
from pathlib import Path
import logging

# Определение пути к файлу JSON с пользователями
USERS_JSON_PATH = Path(__file__).parent.parent.parent / "db" / "users.json"

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Устанавливаем уровень логирования на INFO


# Функция для загрузки пользователей из JSON-файла
def load_users_from_json():
    if not USERS_JSON_PATH.exists():
        return {}  # Возвращаем пустой словарь, если файл не существует
    with open(USERS_JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)  # Загружаем и возвращаем данные из JSON-файла


# Функция для сохранения пользователей в JSON-файл
def save_users_to_json(users):
    with open(USERS_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)  # Записываем данные пользователей в JSON


# Функция для инициализации файла JSON, если он не существует
def init_users_json():
    if not USERS_JSON_PATH.exists():
        with open(USERS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file)  # Создаем пустой JSON-файл


# Инициализация файла JSON при запуске
init_users_json()


# Функция для удаления неактивных пользователей из группы
async def check_inactive_employees(db: Session = next(get_db())):
    # Загружаем пользователей из JSON
    users = load_users_from_json()

    # Получаем всех сотрудников из базы данных
    all_employees = db.query(Employee).all()

    # Проверяем каждого сотрудника на наличие в JSON
    for employee in all_employees:
        telegram_id_str = str(employee.telegram_id)

        if telegram_id_str not in users:
            try:
                # Удаляем пользователя из группы
                await remove_user_from_group(employee.telegram_id, ".........")  # Вставить ID группы
                logging.info(f"Пользователь {telegram_id_str} удален из группы, так как его нет в JSON.")

                # Удаляем пользователя из базы данных
                db.delete(employee)  # Удаляем сотрудника из БД
                db.commit()  # Сохраняем изменения в БД
                logging.info(f"Пользователь {telegram_id_str} удален из базы данных.")
            except Exception as e:
                logging.error(f"Ошибка при удалении пользователя {telegram_id_str} из группы: {e}")
        else:
            logging.info(f"Пользователь {telegram_id_str} присутствует в JSON. Пропуск удаления.")

    # Обновляем JSON (если нужно), чтобы убрать неактуальные записи
    save_users_to_json(users)  # Сохраняем актуальные данные пользователей


# Планировщик
scheduler = AsyncIOScheduler()  # Создаем экземпляр асинхронного планировщика
scheduler.add_job(check_inactive_employees, 'interval', minutes=1)  # Запланируем выполнение функции каждую минуту
scheduler.start()  # Запускаем планировщик