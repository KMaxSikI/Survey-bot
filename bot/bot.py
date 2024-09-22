from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт MemoryStorage
from bot.config import TOKEN
from bot.handlers import questionnaire, admin

# Инициализация бота и диспетчера с хранилищем
bot = Bot(token=TOKEN)  # Создаем экземпляр бота с указанным токеном
storage = MemoryStorage()  # Создаем хранилище в памяти для управления состоянием
dp = Dispatcher(bot, storage=storage)  # Инициализируем диспетчер, передавая ему бота и хранилище

# Настройка обработчиков
questionnaire.register_handlers(dp)  # Регистрируем обработчики для анкеты
admin.register_handlers(dp)  # Регистрируем обработчики для администрирования
