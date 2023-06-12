from aiogram import Dispatcher, executor

from loader import dp, pg
from utils.commands import set_default_commands
from utils.scheduler import check_reminders

import handlers, middlewares, utils
    
    
async def on_startup(dp: Dispatcher):
    await pg.create()
    await set_default_commands(dp)
    
    check_reminders.start()
    

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
