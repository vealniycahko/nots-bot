import os
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiobot.utils.database import create_pool
from aiobot.utils.commands import set_commands
from aiobot.handlers.base import register_base


BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    await create_pool()


def setup(dp: Dispatcher):
    # import aiobot.handlers
    
    logs_path = str(Path(__file__).parent.parent) + '/logs/bot.log'
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_path),
            logging.StreamHandler()
        ]
    )
    
    register_base(dp)
        
    executor.start_polling(dp, on_startup=on_startup)
    
    
# set_commands(bot)

setup(dp)
