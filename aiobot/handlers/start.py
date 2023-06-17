from numdeclination import NumDeclination

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from loader import dp, pg, logger
from keyboards.buttons import start_kbrd, create_kbrd
from utils import emoji


"""
Обработка различных способов запуска команды /start
Запуск команды /start с выводом текущего количества заметок
"""


@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await start(message)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "start_call")
async def start_call(callback_query: CallbackQuery):
    await callback_query.answer()
    # подмена айди бота на айди пользователя
    callback_query.message.from_user.id = callback_query.from_user.id

    await start(callback_query.message)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "cancel_call", state="*"
)
async def start_state_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.finish()
    # подмена айди бота на айди пользователя
    callback_query.message.from_user.id = callback_query.from_user.id

    await start(callback_query.message)


async def start(message: Message):
    query = """ SELECT COUNT(*) FROM notes WHERE owner_id = $1; """
    owner_id = message.from_user.id
    count = await pg.execute(query, owner_id, fetchval=True)

    if count == 0:
        await message.answer(
            text=f"{emoji.folder} На данный момент у тебя нет заметок, но ты можешь создать первую",
            reply_markup=create_kbrd,
        )
    elif count > 0:
        # склонение слова заметка, type = 1 - это именительный падеж
        nd = NumDeclination()
        converted = nd.declinate(count, ["заметка", "заметки", "заметок"], type=1)
        await message.answer(
            text=f"{emoji.folder} У тебя сейчас {converted.number} {converted.word}. \
                Ты можешь создать еще или посмотреть список заметок",
            reply_markup=start_kbrd,
        )
    else:
        logger.error(f"The logic of work is broken. Unexpected count: {count}")
