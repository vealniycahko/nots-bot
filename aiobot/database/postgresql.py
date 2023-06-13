from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from utils import config


"""
Поключение к базе данных

Создание пула соединений (выполняется при запуске бота)
И функция execute для выполнения запросов (для сложных запросов следует создавать дополнительные функции здесь)
"""


class DataBase:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASS,
            host=config.POSTGRES_HOST,
            database=config.POSTGRES_NAME,
            port=config.POSTGRES_PORT
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
