import re
from pydantic import EmailStr, ValidationError

# Проверка валидности email
def validate_email(email: str) -> bool:
    try:
        # Пытаемся проверить email с помощью валидации Pydantic
        EmailStr.validate(email)
        return True  # Если валидация прошла успешно, возвращаем True
    except ValidationError:
        return False  # Если возникла ошибка валидации, возвращаем False

# Проверка валидности номера телефона
def validate_phone(phone: str) -> bool:
    # Определяем регулярное выражение для проверки формата телефона
    pattern = re.compile(r"^\+?\d{10,15}$")
    return bool(pattern.match(phone))  # Возвращаем True, если номер соответствует шаблону, иначе False