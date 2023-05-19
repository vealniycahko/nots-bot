import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import create_pool

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация базы данных
async def on_startup(dp):
    await create_pool()



# Начало работы
@dp.message_handler(commands=['start', 'help', 'info'])
async def start(message: types.Message):
    await message.answer("SHBSKDJVBKVJBVHSBDKVSVCKSVKS")



if __name__ == '__main__':
    # Инициализация логгера
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    
    # Запуск бота
    executor.start_polling(dp, on_startup=on_startup)
