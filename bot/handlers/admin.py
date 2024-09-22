from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from db.models import Employee
from sqlalchemy.orm import Session
from db.database import get_db
from bot.utils.telegram_api import invite_user_to_group_by_link, remove_user_from_group

# Ссылка на группу
GROUP_LINK = "........."  # Заменить на свою ссылку


# Добавление пользователя в группу (если он руководитель)
async def add_user_to_group(message: types.Message, db: Session = next(get_db())):
    user_id = message.from_user.id  # Получаем ID пользователя из сообщения.

    # Пытаемся найти пользователя в базе данных.
    employee = db.query(Employee).filter(Employee.telegram_id == user_id).first()

    if employee and employee.is_manager:  # Если пользователь найден и является руководителем
        await invite_user_to_group_by_link(user_id, GROUP_LINK)  # Приглашаем пользователя в группу по ссылке.
        await message.answer("Вы успешно добавлены в группу руководителей!")  # Уведомляем пользователя о добавлении.
    else:
        await message.answer("У вас нет прав для добавления в эту группу.")  # Если пользователь не руководитель.


# Регистрация нового пользователя через анкету
async def register_user(message: types.Message, state: FSMContext, db: Session = next(get_db())):

    user_id = message.from_user.id  # Получаем ID пользователя из сообщения.

    # Проверяем, существует ли пользователь с таким ID в базе данных.
    existing_employee = db.query(Employee).filter(Employee.telegram_id == user_id).first()

    if existing_employee:  # Если пользователь уже зарегистрирован
        await message.answer("Пользователь с таким ID уже зарегистрирован. Пожалуйста, не повторяйте регистрацию.")  # Отправляем сообщение.
        return


# Удаление пользователя из группы и базы данных
async def remove_user_from_group_handler(message: types.Message, db: Session = next(get_db())):
    user_id = message.from_user.id  # Получаем ID пользователя из сообщения.

    # Пытаемся найти пользователя в базе данных.
    employee = db.query(Employee).filter(Employee.telegram_id == user_id).first()

    if employee and not employee.active:  # Если пользователь найден и не активен (уволен)
        await remove_user_from_group(user_id, ".........")  # Удаляем пользователя из группы по ID чата.
        db.delete(employee)  # Удаляем запись пользователя из базы данных.
        db.commit()  # Применяем изменения к базе данных.
        await message.answer("Вы были удалены из группы и базы данных, так как вы больше не числитесь действующим сотрудником.")  # Уведомляем пользователя об удалении.
    else:
        await message.answer("Вы активный сотрудник или не найдены в базе.")  # Если пользователь активен или не найден.


# Регистрация функций обработки команд
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_user_to_group, commands="add_to_group", state="*")  # Добавление в группу.
    dp.register_message_handler(remove_user_from_group_handler, commands="remove_from_group", state="*")  # Удаление из группы.
    dp.register_message_handler(register_user, commands="register", state="*")  # Регистрация пользователя.
