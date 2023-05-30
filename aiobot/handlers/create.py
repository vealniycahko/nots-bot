from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, pg


class CreateNoteStates(StatesGroup):
    WAITING_TITLE = State()
    WAITING_TEXT = State()
    WAITING_TIME = State()


@dp.message_handler(commands=['create'])
async def create_note(message: Message, state: FSMContext):
    await message.answer('Введи название заметки')

    await state.set_state(CreateNoteStates.WAITING_TITLE)


@dp.message_handler(state=CreateNoteStates.WAITING_TITLE)
async def get_note_title(message: Message, state: FSMContext):
    note_title = message.text
    
    if len(note_title) > 100:
        await message.answer('О, нет! Можно не больше 100 символов... Попробуй еще раз')      
    else:
        await message.answer('Окей, теперь описание заметки')
        await state.update_data(title=note_title)
        await state.set_state(CreateNoteStates.WAITING_TEXT)
        
        
@dp.message_handler(state=CreateNoteStates.WAITING_TEXT)
async def get_note_text(message: Message, state: FSMContext):
    note_text = message.text
    
    await message.answer('И последнее, дата напоминания в формате "дд.мм.гггг чч:мм"')
    await state.update_data(text=note_text)
    await state.set_state(CreateNoteStates.WAITING_TIME)


# @dp.message_handler(state=CreateNoteStates.WAITING_TIME)
# async def get_reminder_time(message: Message, state: FSMContext, pool: Pool):
#     note_time = message.text
    
#     try:
#         time_obj = datetime.strptime(note_time, '%d.%m.%Y %H:%M')
#         data = await state.get_data()
        
#         note_title = data.get('title')
#         note_text = data.get('text')
#         owner_id = message.from_user.id
        
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO notes (owner_id, note_title, note_text, reminder_time) VALUES ($1, $2, $3, $4)',
#                 owner_id, note_title, note_text, time_obj
#             )
            
#         await message.answer('Успех! Заметка создана')
#         await state.finish()
        
#     except (ValueError, TypeError):
#         await message.answer('Неверный формат даты и времени :( Попробуй еще раз')
