from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, pg
from keyboards.buttons import skip_update_kbrd, skip_clean_update_kbrd, return_kbrd


class ChangeNoteStates(StatesGroup):
    WAITING_NEW_TITLE = State()
    WAITING_NEW_TEXT = State()
    WAITING_NEW_TIME = State()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('change'))
async def start_changing(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    query = """ SELECT * FROM notes WHERE id = $1; """
    note_id = int(callback_query.data[6:])
    note = await pg.execute(query, note_id, fetchrow=True)
    
    await state.set_state(ChangeNoteStates.WAITING_NEW_TITLE)
    
    await state.update_data(note_id=note_id)
    await state.update_data(old_text=note['note_text'])
    await state.update_data(old_time=note['reminder_time'])
    
    await callback_query.message.answer(
        text=f'Название заметки:\n*{note["note_title"]}*\nНапиши новое название, либо нажми "Пропустить", чтобы оставить его прежним',
        reply_markup=skip_update_kbrd,
        parse_mode='Markdown'
    )


@dp.message_handler(state=ChangeNoteStates.WAITING_NEW_TITLE)
async def get_new_title(message: Message, state: FSMContext):
    note_title = message.text
    
    if note_title and len(note_title) > 100:
        await message.answer(
            text='О, нет! Допустимо не более 100 символов. Попробуй еще раз',
            reply_markup=skip_update_kbrd
        )      
    else:
        data = await state.get_data()
        old_text = data.get('old_text')
        
        if old_text:
            await message.answer(
                text=f'Переходим к описанию:\n*{old_text}*\nМожешь отправить новое, пропустить этот шаг, либо убрать описание',
                reply_markup=skip_clean_update_kbrd,
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                text='Переходим к описанию. У этой заметки нет описания, но можно написать описание для заметки, либо пропустить этот шаг',
                reply_markup=skip_update_kbrd)
        
        await state.update_data(new_title=note_title)
        await state.set_state(ChangeNoteStates.WAITING_NEW_TEXT)
        
        
@dp.message_handler(state=ChangeNoteStates.WAITING_NEW_TEXT)
async def get_new_text(message: Message, state: FSMContext):
    note_text = message.text
    
    data = await state.get_data()
    old_time = data.get('old_time')
    
    if old_time:
        await message.answer(
            text=f'Время напоминания:\n{old_time.strftime("%d.%m.%Y %H:%M")}\nВведи новое время в формате "дд.мм.гггг чч:мм", пропусти этот шаг или удали время',
            reply_markup=skip_clean_update_kbrd
        )
    else:
        await message.answer(
            text='У этой заметки нет времени напоминания, но ты можешь его создать: введи его в формате "дд.мм.гггг чч:мм"',
            reply_markup=skip_update_kbrd
        )
    
    await state.update_data(new_text=note_text)
    await state.set_state(ChangeNoteStates.WAITING_NEW_TIME)


@dp.message_handler(state=ChangeNoteStates.WAITING_NEW_TIME)
async def get_new_time(message: Message, state: FSMContext):
    note_time = message.text
    
    if note_time:
        try:
            note_time = datetime.strptime(note_time, '%d.%m.%Y %H:%M')
            
            if note_time <= datetime.now():
                await message.answer(
                    text='Это время выбрать невозможно, оно уже прошло...',
                    reply_markup=skip_update_kbrd
                )
                return
        except ValueError:
            await message.answer(
                text='Неверный формат даты и времени :( Попробуй еще раз',
                reply_markup=skip_update_kbrd
            )
        
    data = await state.get_data()
    
    note_title = data.get('new_title')
    note_text = data.get('new_text')
    note_id = data.get('note_id')
    
    if note_title != False:
        query = """ UPDATE notes SET note_title = $1 WHERE id = $2; """
        await pg.execute(query, note_title, note_id, execute=True)
    if note_text != False:
        query = """ UPDATE notes SET note_text = $1 WHERE id = $2; """
        await pg.execute(query, note_text, note_id, execute=True)
    if note_time != False:
        query = """ UPDATE notes SET reminder_time = $1 WHERE id = $2; """
        await pg.execute(query, note_time, note_id, execute=True)
        
    await message.answer(
        text='Заметка успешно обновлена!',
        reply_markup=return_kbrd
    )
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'skip_update_call', state='*')
async def skip_note_update(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    callback_query.message.text = False
    
    current_state = await state.get_state()
    if current_state == 'ChangeNoteStates:WAITING_NEW_TITLE':
        await get_new_title(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TEXT':
        await get_new_text(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TIME':
        await get_new_time(callback_query.message, state)
    
    
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'clean_update_call', state='*')
async def clean_note_update(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    callback_query.message.text = None
    
    current_state = await state.get_state()
    if current_state == 'ChangeNoteStates:WAITING_NEW_TEXT':
        await get_new_text(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TIME':
        await get_new_time(callback_query.message, state)
