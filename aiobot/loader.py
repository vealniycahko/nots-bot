from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import config
from databases.postgresql import PostgresDB
from databases.redis import RedisDB
from utils import logging

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
pg = PostgresDB()
rd = RedisDB()
logger = logging.logger