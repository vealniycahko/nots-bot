from aiogram import Dispatcher, executor

from loader import dp, pg, rd
from utils.commands import set_default_commands
from utils.scheduler import check_reminders

import handlers, middlewares  # для инициализации


async def on_startup(dp: Dispatcher):
    await pg.create()
    await rd.create()
    await set_default_commands(dp)

    check_reminders.start()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
