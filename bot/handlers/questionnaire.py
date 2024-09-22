from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Employee
from bot.utils.validators import validate_phone, validate_email
from bot.utils.telegram_api import invite_user_to_group_by_link
from bot.utils.json_handler import save_users_to_json, load_users_from_json
import json
from pathlib import Path

# Определение путей и загрузка правил статуса
STATUS_RULES_PATH = Path(__file__).parent.parent.parent / "db" / "status_rules.json"
with open(STATUS_RULES_PATH, "r", encoding="utf-8") as file:
    status_rules = json.load(file)  # Загружаем правила статуса из JSON-файла


# Определение состояний анкеты
class FSMQuestionnaire(StatesGroup):
    full_name = State()  # Состояние для ввода ФИО
    phone = State()  # Состояние для ввода телефона
    email = State()  # Состояние для ввода email
    position = State()  # Состояние для ввода должности
    department = State()  # Состояние для ввода департамента


# Начало анкеты
async def start_questionnaire(message: types.Message):
    await FSMQuestionnaire.full_name.set()  # Устанавливаем состояние для ввода ФИО
    await message.answer("Пожалуйста, введите ваше ФИО полностью (Максимов Петр Владиславович):")  # Запрашиваем ФИО у пользователя


# Обработка ФИО
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)  # Сохраняем ФИО в состоянии
    await FSMQuestionnaire.next()  # Переходим к следующему состоянию
    await message.answer("Пожалуйста, введите ваш мобильный телефон (в формате +79998887766):")


# Обработка номера телефона
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.text  # Получаем номер телефона
    if validate_phone(phone_number):  # Проверяем формат номера телефона
        await state.update_data(phone=phone_number)  # Сохраняем номер в состоянии
        await FSMQuestionnaire.next()  # Переходим к следующему состоянию
        await message.answer("Пожалуйста, введите вашу рабочую почту (например, name@example.com):")
    else:
        await message.answer("Неверный формат номера телефона. Пожалуйста, введите номер в формате +79998887766.")


# Обработка рабочей почты
async def process_email(message: types.Message, state: FSMContext):
    email = message.text  # Получаем email
    if validate_email(email):  # Проверяем формат email
        await state.update_data(email=email)  # Сохраняем email в состоянии
        await FSMQuestionnaire.next()  # Переходим к следующему состоянию
        await message.answer("Пожалуйста, введите вашу должность в компании:")
    else:
        await message.answer("Неверный формат почты. Пожалуйста, введите корректный email (например, name@example.com).")


# Обработка должности
async def process_position(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)  # Сохраняем должность в состоянии
    await FSMQuestionnaire.next()  # Переходим к следующему состоянию
    await message.answer("Пожалуйста, введите ваше подразделение:")


# Обработка департамента и завершение анкеты
async def process_department(message: types.Message, state: FSMContext, db: Session = next(get_db())):
    await state.update_data(department=message.text)  # Сохраняем департамент в состоянии
    user_data = await state.get_data()  # Получаем данные из состояния

    # Проверяем, существует ли пользователь в базе данных
    existing_employee = db.query(Employee).filter(Employee.telegram_id == message.from_user.id).first()
    if existing_employee:
        await message.answer("Пользователь с таким ID уже зарегистрирован. Пожалуйста, не повторяйте регистрацию.")
        await state.finish()  # Завершаем состояние
        return

    try:
        # Создание записи сотрудника
        employee = Employee(
            full_name=user_data['full_name'],
            phone=user_data['phone'],
            email=user_data['email'],
            position=user_data['position'],
            department=user_data['department'],
            telegram_id=message.from_user.id
        )

        # Проверка, является ли сотрудник руководителем
        if employee.position in status_rules["manager_positions"]:
            employee.is_manager = True

        # Добавление и сохранение сотрудника в базе данных
        db.add(employee)  # Добавляем нового сотрудника
        db.commit()  # Сохраняем изменения в базе данных
        db.refresh(employee)  # Обновляем данные сотрудника

        # Сохранение данных сотрудника в JSON-файл
        users = load_users_from_json()  # Загружаем существующих пользователей из JSON
        users[str(employee.telegram_id)] = {
            "full_name": employee.full_name,
            "phone": employee.phone,
            "email": employee.email,
            "position": employee.position,
            "department": employee.department,
        }
        save_users_to_json(users)  # Сохраняем обновлённый список пользователей

        # Завершение состояния
        await state.finish()

        # Логика уведомлений о статусе и приглашение в группу
        if employee.is_manager:
            await message.answer(f"Поздравляем, {employee.full_name}! Примите приглашение в группу руководителей.")
            await invite_user_to_group_by_link(employee.telegram_id, ".........")  # Заменить на свою ссылку
        else:
            await message.answer("Вам отказано в вступлении в группу, в группу могут вступать только руководители.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")  # Обработка ошибок


# Настройка обработчиков
def register_handlers(dp):
    dp.register_message_handler(start_questionnaire, commands="start", state="*")  # Обработчик для команды /start
    dp.register_message_handler(process_full_name, state=FSMQuestionnaire.full_name)  # Обработчик для ввода ФИО
    dp.register_message_handler(process_phone, state=FSMQuestionnaire.phone)  # Обработчик для ввода телефона
    dp.register_message_handler(process_email, state=FSMQuestionnaire.email)  # Обработчик для ввода email
    dp.register_message_handler(process_position, state=FSMQuestionnaire.position)  # Обработчик для ввода должности
    dp.register_message_handler(process_department, state=FSMQuestionnaire.department)  # Обработчик для ввода департамента

