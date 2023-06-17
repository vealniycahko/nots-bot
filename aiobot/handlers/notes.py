from datetime import timedelta

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from loader import dp, pg, rd
from keyboards.notes import notes_inline_kbrd, single_note_kbrd
from keyboards.buttons import return_kbrd
from utils import emoji


"""
Вывод и управление заметками:

Вывод всех заметок с помощью инлайн клавиатуры
Вывод данных заметки (обработка коллбэков)
Удаление заметки из базы данных
"""


@dp.message_handler(commands=["notes"])
async def notes_list_command(message: Message):
    await notes_list(message)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "notes_call")
async def notes_list_call(callback_query: CallbackQuery):
    await callback_query.answer()
    callback_query.message.from_user.id = callback_query.from_user.id

    await notes_list(callback_query.message)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "notes_call", state="*"
)
async def notes_list_state(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    callback_query.message.from_user.id = callback_query.from_user.id
    await state.finish()

    await notes_list(callback_query.message)


async def notes_list(message: Message):
    # максимальное количество инлайн кнопок - 100 штук
    # на данном этапе целесообразно просто ограничить это с помощью LIMIT
    query = """
        SELECT * FROM notes WHERE owner_id = $1
        ORDER BY reminder_time ASC
        LIMIT 95;
    """
    value = message.from_user.id
    notes = await pg.execute(query, value, fetch=True)

    tz = (
        await rd.get_tz(message.from_user.id) or 3
    )  # такой ситуации не должно возникать, это подстраховка

    kbrd = await notes_inline_kbrd(notes, tz)

    await message.answer(
        text=f"{emoji.manuscript} Нажми на заметку, чтобы посмотреть, изменить или удалить ее",
        reply_markup=kbrd,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("open")
)
async def open_note(callback_query: CallbackQuery):
    await callback_query.answer()

    query = """ SELECT * FROM notes WHERE id = $1; """
    note_id = callback_query.data[4:]
    note = await pg.execute(query, note_id, fetchrow=True)

    tz = await rd.get_tz(callback_query.message.from_user.id) or 3

    text = f'*{note["note_title"]}*'
    if note["note_text"]:
        text += f'\n{note["note_text"]}'
    if note["reminder_time"]:
        reminder_time = note["reminder_time"] + timedelta(hours=int(tz))
        text += f'\n{reminder_time.strftime("%d.%m.%Y %H:%M")}'

    kbrd = await single_note_kbrd(note["id"])

    await callback_query.message.answer(
        text=text, reply_markup=kbrd, parse_mode="Markdown"
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("delete")
)
async def dalete_note_call(callback_query: CallbackQuery):
    await callback_query.answer()
    await dalete_note(callback_query)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("delete"), state="*"
)
async def dalete_note_state(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.finish()
    await dalete_note(callback_query)


async def dalete_note(callback_query: CallbackQuery):
    query = """ DELETE FROM notes WHERE id = $1; """
    note_id = callback_query.data[6:]
    await pg.execute(query, note_id, execute=True)

    await callback_query.message.answer(
        text=f"{emoji.greencross} Заметка успешно уделена", reply_markup=return_kbrd
    )
