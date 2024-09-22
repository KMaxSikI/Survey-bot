'''Функционал не реализован, возможна будущая доработка при необходимости'''

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопка подтверждения анкеты
def get_confirmation_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)  # Создаем инлайн-клавиатуру с шириной строки 2
    # Создаем кнопку "Подтвердить" с callback_data для обработки нажатия
    confirm_button = InlineKeyboardButton(text="Подтвердить", callback_data="confirm")
    # Создаем кнопку "Отмена" с callback_data для обработки нажатия
    cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    # Добавляем кнопки на клавиатуру
    keyboard.add(confirm_button, cancel_button)
    return keyboard  # Возвращаем готовую клавиатуру
