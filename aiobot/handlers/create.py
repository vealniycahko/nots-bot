from datetime import datetime
from typing import assert_never

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, pg
from keyboards.buttons import skip_cancel_kbrd, cancel_kbrd, return_kbrd
from utils import emoji


"""
Полный цикл создания заметки, включая класс состояний
и обработку коллбэков при пропуске какого-либо этапа
"""


class CreateNoteStates(StatesGroup):
    WAITING_TITLE = State()
    WAITING_TEXT = State()
    WAITING_TIME = State()


@dp.message_handler(commands=['create'])
async def create_note_command(message: Message, state: FSMContext):
    await create_note(message, state)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'create_call')
async def create_note_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await create_note(callback_query.message, state)

async def create_note(message: Message, state: FSMContext):
    await message.answer(
        text=f'{emoji.pushpin} Введи название заметки',
        reply_markup=cancel_kbrd
    )
    
    await state.set_state(CreateNoteStates.WAITING_TITLE)


@dp.message_handler(state=CreateNoteStates.WAITING_TITLE)
async def get_note_title(message: Message, state: FSMContext):
    note_title = message.text
    
    if len(note_title) > 100:
        await message.answer(
            text=f'{emoji.exclaim} О, нет! Допустимо не более 100 символов. Попробуй еще раз',
            reply_markup=cancel_kbrd
        )      
    else:
        await message.answer(
            text=f'{emoji.pushpin} Продолжаем, теперь описание заметки',
            reply_markup=skip_cancel_kbrd
        )
        
        await state.update_data(title=note_title)
        await state.set_state(CreateNoteStates.WAITING_TEXT)
        
        
@dp.message_handler(state=CreateNoteStates.WAITING_TEXT)
async def get_note_text(message: Message, state: FSMContext):
    note_text = message.text
    
    await message.answer(
        text=f'{emoji.pushpin} Последнее, дата напоминания в формате "дд.мм.гггг чч:мм"',
        reply_markup=skip_cancel_kbrd
    )
    
    await state.update_data(text=note_text)
    await state.set_state(CreateNoteStates.WAITING_TIME)


@dp.message_handler(state=CreateNoteStates.WAITING_TIME)
async def get_reminder_time(message: Message, state: FSMContext):
    note_time = message.text
    
    if note_time:
        try:
            note_time = datetime.strptime(note_time, '%d.%m.%Y %H:%M')
            if note_time <= datetime.now():
                await message.answer(
                    text=f'{emoji.exclaim} Это время выбрать невозможно, оно уже прошло...',
                    reply_markup=skip_cancel_kbrd
                )
                return
        except ValueError:
            await message.answer(
                text=f'{emoji.exclaim} Неверный формат даты и времени... Попробуй еще раз',
                reply_markup=skip_cancel_kbrd
            )
            return
    
    data = await state.get_data()
    
    note_title = data.get('title')
    note_text = data.get('text')
    owner_id = message.from_user.id
    
    query = """ INSERT INTO notes (owner_id, note_title, note_text, reminder_time) VALUES ($1, $2, $3, $4); """
    values = (owner_id, note_title, note_text, note_time)
    await pg.execute(query, *values, execute=True)
        
    await message.answer(
        text=f'{emoji.checkmark} Успех! Заметка создана',
        reply_markup=return_kbrd
    )
    
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'skip_data_call', state = '*')
async def skip_creation_step(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    # отсутствие значения message.text при пропуске этапа
    callback_query.message.text = None
    # подмена айди бота на айди пользователя для внесения в базу данных
    callback_query.message.from_user.id = callback_query.from_user.id 
    
    current_state = await state.get_state()
    if current_state == 'CreateNoteStates:WAITING_TEXT':
        await get_note_text(callback_query.message, state)
    elif current_state == 'CreateNoteStates:WAITING_TIME':
        await get_reminder_time(callback_query.message, state)
    else:
        assert_never(current_state)