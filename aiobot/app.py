from aiogram import Dispatcher, executor

from loader import dp, pg
import handlers, utils
from utils.commands import set_default_commands


async def on_startup(dp: Dispatcher):
    await pg.create()
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
