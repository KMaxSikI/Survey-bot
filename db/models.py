from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base


class Employee(Base):
    __tablename__ = 'employees'  # Указываем имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Идентификатор сотрудника, первичный ключ
    full_name = Column(String, nullable=False)  # Полное имя сотрудника, не может быть пустым
    phone = Column(String, nullable=False, unique=True)  # Номер телефона, уникальный и не может быть пустым
    email = Column(String, nullable=False, unique=True)  # Email, уникальный и не может быть пустым
    position = Column(String, nullable=False)  # Должность сотрудника, не может быть пустой
    department = Column(String, nullable=False)  # Подразделение, не может быть пустым
    is_manager = Column(Boolean, default=False)  # Статус "Руководитель", по умолчанию False
    active = Column(Boolean, default=True)  # Статус "Действующий сотрудник", по умолчанию True
    telegram_id = Column(Integer, unique=True, nullable=True)  # ID пользователя Telegram, уникальный, может быть пустым

    def __repr__(self):
        return f"<Employee(name={self.full_name}, position={self.position}, active={self.active})>"  # Представление объекта для удобного отображения
