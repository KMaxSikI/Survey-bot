from aiogram import Bot

# Инициализация бота (нужно вставить токен своего бота)
bot = Bot(token=".........................")  # Создаем экземпляр бота с токеном

# Функция для приглашения пользователя в группу
async def invite_user_to_group_by_link(user_id, group_link):
    try:
        # Отправка ссылки на группу пользователю
        await bot.send_message(user_id, f"Вы приглашены в группу: {group_link}")
    except Exception as e:
        # Логирование ошибки, если не удалось отправить сообщение
        print(f"Ошибка при приглашении пользователя: {e}")

# Функция для удаления пользователя из группы
async def remove_user_from_group(telegram_id: int, chat_id: str):
    try:
        # Исключаем пользователя из группы по его ID
        await bot.ban_chat_member(chat_id=chat_id, user_id=telegram_id)
        print(f"Пользователь {telegram_id} был удален из группы {chat_id}.")  # Логирование успешного удаления
    except Exception as e:
        # Логирование ошибки, если не удалось удалить пользователя
        print(f"Ошибка при удалении пользователя из группы: {e}")


