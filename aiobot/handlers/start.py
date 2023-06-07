from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from loader import dp, pg
from keyboards.buttons import start_kbrd, create_kbrd


@dp.message_handler(commands=['start'])
async def create_note(message: Message):
    await start(message)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'start_call')
async def create_note_call(callback_query: CallbackQuery):
    await callback_query.answer()
    callback_query.message.from_user.id = callback_query.from_user.id
    await start(callback_query.message)
    

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'cancel_call', state='*')
async def cancel_creation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.finish()
    callback_query.message.from_user.id = callback_query.from_user.id

    await start(callback_query.message)
 
 
async def start(message: Message):
    query = """ SELECT COUNT(*) FROM notes WHERE OWNER_ID = $1; """
    owner_id = message.from_user.id
    count = await pg.execute(query, owner_id, fetchval=True)
    
    if count == 0:
        await message.answer(f'На данный момент у тебя нет заметок, но ты можешь создать первую', reply_markup=create_kbrd)
    else:
        await message.answer(f'У тебя сейчас {count} заметок. Ты можешь создать еще или посмотреть список заметок', reply_markup=start_kbrd)
    