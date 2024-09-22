from aiogram import executor
from bot.bot import dp
from bot.utils import scheduler  # Импортируем планировщик, чтобы он инициализировался
from db.database import init_db  # Импорт функции инициализации базы данных

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()  # Вызываем функцию для создания таблиц в базе данных

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)  # Начинаем опрос новых обновлений с пропуском старых
