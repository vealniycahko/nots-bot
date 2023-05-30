from aiogram import Dispatcher
from aiogram.types import Message

    
def register_base(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def start(message: Message):
        await message.answer('Тут будет...')
    