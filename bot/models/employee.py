from pydantic import BaseModel, EmailStr, constr


# Модель для валидации данных анкеты
class EmployeeModel(BaseModel):
    full_name: str  # Полное имя сотрудника
    phone: constr(regex=r"^\+?\d{10,15}$")  # Валидация телефона: должен начинаться с '+' (необязательно) и содержать от 10 до 15 цифр
    email: EmailStr  # Валидация электронной почты с использованием встроенного типа EmailStr
    position: str  # Должность сотрудника
    department: str  # Подразделение, в котором работает сотрудник


# Модель для обновления статуса сотрудника
class UpdateStatusModel(BaseModel):
    status: str  # Поле для хранения статуса сотрудника
