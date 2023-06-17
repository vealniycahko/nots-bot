from aiogram.types import Message, CallbackQuery

from loader import dp, rd
from keyboards.buttons import tzone_kbrd, return_kbrd
from keyboards.timezone import time_zone_kbrd
from utils import emoji


"""
Просмотр и изменение часового пояса пользователя
"""


@dp.message_handler(commands=["timezone"])
async def timezone_command(message: Message):
    await timezone(message)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "time_zone_call"
)
async def timezone_call(callback_query: CallbackQuery):
    await callback_query.answer()
    callback_query.message.from_user.id = callback_query.from_user.id
    await timezone(callback_query.message)


async def timezone(message: Message):
    tz = await rd.get_tz(message.from_user.id)

    if tz:
        await message.answer(
            text=f"{emoji.clock} Твой часовой пояс: UTC {int(tz)}:00",
            reply_markup=tzone_kbrd,
        )
    else:
        await message.answer(
            text=f"{emoji.clock} У тебя сейчас не задан часовой пояс...",
            reply_markup=tzone_kbrd,
        )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "modify_timezone_call"
)
async def modify_timezone_call(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.answer(
        text=f"{emoji.pushpin} Выбери свой часовой пояс в формате UTC (ты сможешь его изменить)\n\
            Часовой пояс Москвы по UTC - +3:00 и так далее",
        reply_markup=time_zone_kbrd,
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("tz"))
async def get_time_zone(callback_query: CallbackQuery):
    await callback_query.answer()

    tz = int(callback_query.data[2:])
    await rd.set_tz(callback_query.from_user.id, tz)

    await callback_query.message.answer(
        text=f"{emoji.checkmark} Часовой пояс успешно изменен на UTC {int(tz)}:00",
        reply_markup=return_kbrd,
    )
