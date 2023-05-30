import os
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncpg.pool import Pool

from aiobot.utils.database import create_pool


BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

pool = create_pool()


def register_handlers(dp: Dispatcher, pool: Pool):
    from aiobot.handlers.base import register_base
    from aiobot.handlers.create import register_create
    
    register_base(dp, pool)
    register_create(dp, pool)



def setup(dp: Dispatcher, pool: Pool):  
    logs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'bot.log')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_path),
            logging.StreamHandler()
        ]
    )
    
    register_handlers(dp, pool)
    
    executor.start_polling(dp)


setup(dp, pool)
