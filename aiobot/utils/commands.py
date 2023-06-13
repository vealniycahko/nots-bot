from aiogram import Dispatcher
from aiogram.types import BotCommand


"""
Установка команд для быстрого доступа

Запускается при старте бота
"""


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'просто начать'),
            BotCommand('notes', 'просмотр заметок'),
            BotCommand('create', 'создать заметку'),
        ]
    )