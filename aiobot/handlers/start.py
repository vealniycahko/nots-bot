from aiogram.types import Message

from loader import dp, pg
from keyboards.buttons import start_kbrd
    
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer('Тут будет...', reply_markup=start_kbrd)
    