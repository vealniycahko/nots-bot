from typing import Union

from aioredis import Redis, from_url

from utils import config


"""
Подключение к базе данных Redis

Создание пула соединений (выполняется при запуске бота)
Две функции: внести часовой пояс пользователя и получить его
"""


class RedisDB:
    def __init__(self):
        self.pool: Union[Redis, None] = None

    async def create(self):
        redis_url = f"redis://:{config.REDIS_PASS}@{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
        self.pool = await from_url(redis_url, encoding=config.REDIS_ENCODING)

    async def set_tz(self, key: int, value: int):
        await self.pool.set(key, value)

    async def get_tz(self, key: int):
        return await self.pool.get(key)
