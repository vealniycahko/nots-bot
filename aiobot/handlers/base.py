from aiogram import Dispatcher
from aiogram.types import Message

# from aiobot.__main__ import dp

# def setup(dp: Dispatcher):

def register_base(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def start(message: Message):
        await message.answer('Тут будет...')

    @dp.message_handler()
    async def echo_message(message: Message):
        await message.answer(message.text)
        
    # dp.register_message_handler(start, commands=['start'])
    # dp.register_message_handler(echo_message)


# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(start, commands=['start'])
#     dp.register_message_handler(echo_message)


    