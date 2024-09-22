from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Путь к базе данных SQLite
DATABASE_URL = "sqlite:///db/test.db"  # Указываем путь к файлу базы данных SQLite
print(f"Используемая база данных: {DATABASE_URL}")  # Проверка и вывод используемого пути к базе данных

# Создание движка базы данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Создаем движок с параметрами подключения

# Создание базового класса для моделей
Base = declarative_base()  # Создаем базовый класс для определения моделей базы данных

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создаем фабрику сессий с заданными параметрами


# Автоматическое создание таблиц в базе данных при запуске
def init_db():
    import db.models  # Импорт моделей перед созданием таблиц, чтобы все модели были доступны
    Base.metadata.create_all(bind=engine)  # Создаем все таблицы, описанные в моделях, если они не существуют
    print("Таблицы созданы или уже существуют.")  # Сообщение о создании таблиц или их существовании


# Получение сессии базы данных
def get_db():
    db = SessionLocal()  # Создаем новую сессию
    try:
        yield db  # Возвращаем сессию для использования
    finally:
        db.close()  # Закрываем сессию после завершения работы


# Инициализация базы данных при запуске
init_db()  # Вызываем функцию инициализации базы данных для создания таблиц
