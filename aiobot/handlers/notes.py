from aiogram.types import Message, CallbackQuery

from loader import dp, pg
from keyboards.notes import notes_inline_kbrd, single_note_kbrd


@dp.message_handler(commands=['notes'])
async def create_note(message: Message):
    await notes_handler(message )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'notes_call')
async def create_note_call(callback_query: CallbackQuery):
    await callback_query.answer()
    callback_query.message.from_user.id = callback_query.from_user.id
    
    await notes_handler(callback_query.message)


async def notes_handler(message: Message):
    query = """ SELECT * FROM notes WHERE owner_id = $1
        ORDER BY reminder_time ASC; """
    value = message.from_user.id
    notes = await pg.execute(query, value, fetch=True)
    
    kbrd = await notes_inline_kbrd(notes)

    await message.answer(text='Нажми на заметку, чтобы посмотреть, изменить или удалить ее', reply_markup=kbrd)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('open'))
async def handle_every_note(callback_query: CallbackQuery):
    await callback_query.answer()
    
    query = """ SELECT * FROM notes WHERE id = $1; """
    note_id = int(callback_query.data[4:])
    note = await pg.execute(query, note_id, fetchrow=True)
    
    text = f'{note["note_title"]}'
    if note["note_text"]:
        text += f'\n{note["note_text"]}'
    if note["reminder_time"]:
        text += f'\n{note["reminder_time"].strftime("%d.%m.%Y %H:%M")}'
    
    kbrd = await single_note_kbrd(note['id'])
    
    await callback_query.message.answer(text=text, reply_markup=kbrd)
