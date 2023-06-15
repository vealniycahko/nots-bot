from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, pg, rd, logger
from keyboards.buttons import skip_update_kbrd, skip_clean_update_kbrd, return_kbrd
from keyboards.timezone import time_zone_kbrd
from utils import emoji


"""
В этом модуле хендлеры для цикла обновления данных заметки,

включая обработку коллбэков пропуска этапа и удаления текущего значения,
а также получение часового пояса пользователя, если он не задан
"""


class ChangeNoteStates(StatesGroup):
    WAITING_NEW_TITLE = State()
    WAITING_NEW_TEXT = State()
    WAITING_NEW_TIME = State()
    WAITING_TZ = State()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('change'))
async def start_change(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    query = """ SELECT * FROM notes WHERE id = $1; """
    note_id = callback_query.data[6:]
    note = await pg.execute(query, note_id, fetchrow=True)
        
    await state.update_data(note_id=note_id)
    await state.update_data(old_text=note['note_text'])
    await state.update_data(old_time=note['reminder_time'])
    
    await callback_query.message.answer(
        text=f'{emoji.pushpin} Название заметки:\n\n*{note["note_title"]}*\n\nНапиши новое название, либо нажми "Пропустить", чтобы оставить его прежним',
        reply_markup=skip_update_kbrd,
        parse_mode='Markdown'
    )
    
    await state.set_state(ChangeNoteStates.WAITING_NEW_TITLE)


@dp.message_handler(state=ChangeNoteStates.WAITING_NEW_TITLE)
async def get_new_title(message: Message, state: FSMContext):
    note_title = message.text
    
    if note_title and len(note_title) > 100:
        await message.answer(
            text=f'{emoji.exclaim} О, нет! Допустимо не более 100 символов. Попробуй еще раз',
            reply_markup=skip_update_kbrd
        )      
    else:
        data = await state.get_data()
        old_text = data.get('old_text')
        
        if old_text:
            await message.answer(
                text=f'{emoji.pushpin} Переходим к описанию:\n\n*{old_text}*\n\nМожешь отправить новое, пропустить этот шаг, либо убрать описание',
                reply_markup=skip_clean_update_kbrd,
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                text=f'{emoji.pushpin} Переходим к описанию. У этой заметки нет описания, но можно создать его, либо пропустить этот шаг',
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
            text=f'{emoji.pushpin} Время напоминания:\n\n{old_time.strftime("%d.%m.%Y %H:%M")}\n\nВведи новое время в формате "дд.мм.гггг чч:мм", пропусти этот шаг или удали время',
            reply_markup=skip_clean_update_kbrd
        )
    else:
        await message.answer(
            text=f'{emoji.pushpin} У этой заметки нет времени напоминания, но ты можешь его создать: напиши его в формате "дд.мм.гггг чч:мм"',
            reply_markup=skip_update_kbrd
        )
    
    await state.update_data(new_text=note_text)
    await state.set_state(ChangeNoteStates.WAITING_NEW_TIME)


@dp.message_handler(state=ChangeNoteStates.WAITING_NEW_TIME)
async def get_new_time(message: Message, state: FSMContext):
    note_time = message.text
    await state.update_data(new_time=note_time)
    
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    
    if note_time:
        try:
            note_time = datetime.strptime(note_time, '%d.%m.%Y %H:%M')
        except ValueError:
            await message.answer(
                text=f'{emoji.exclaim} Неверный формат даты и времени... Попробуй еще раз',
                reply_markup=skip_update_kbrd
            )
            return
    
        await state.update_data(new_time=note_time)
        
        tz = await rd.get_tz(user_id)
        
        if tz:
            offset = timedelta(hours=int(tz))
            note_time = note_time - offset
            await state.update_data(new_time=note_time)
            await complete_updating(message, state)
        else:
            await message.answer(
                text=f'{emoji.pushpin} Выбери свой часовой пояс в формате UTC(ты сможешь его изменить)\nЧасовой пояс Москвы по UTC - +3:00 и так далее',
                reply_markup=time_zone_kbrd
            )
            await state.set_state(ChangeNoteStates.WAITING_TZ)
    else:
        await complete_updating(message, state)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('tz'), state=ChangeNoteStates.WAITING_TZ)
async def get_time_zone(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    data = await state.get_data()
    user_id = data.get('user_id')
    note_time = data.get('new_time')
    
    tz = int(callback_query.data[2:])
    await rd.set_tz(user_id, tz)
    
    offset = timedelta(hours=tz)
    note_time = note_time - offset
    await state.update_data(new_time=note_time)
    await complete_updating(callback_query.message, state)
    
    
async def complete_updating(message: Message, state: FSMContext):    
    data = await state.get_data()
    
    note_title = data.get('new_title')
    note_text = data.get('new_text')
    note_time = data.get('new_time')
    note_id = data.get('note_id')
    
    # проверка != False, чтобы выполнять действие при значении None, в том числе
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
        text=f'{emoji.checkmark} Заметка успешно обновлена!',
        reply_markup=return_kbrd
    )
    
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'skip_update_call', state = '*')
async def skip_note_update(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    # так как None используется для обнуления значения, тут False (это учитывается в get_new_time())
    callback_query.message.text = False
    callback_query.message.from_user.id = callback_query.from_user.id
    
    current_state = await state.get_state()
    if current_state == 'ChangeNoteStates:WAITING_NEW_TITLE':
        await get_new_title(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TEXT':
        await get_new_text(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TIME':
        await get_new_time(callback_query.message, state)
    else:
        logger.error(f'The logic of work is broken. Unexpected state: {current_state}')
    
    
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'clean_update_call', state = '*')
async def clean_note_update(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    callback_query.message.text = None
    callback_query.message.from_user.id = callback_query.from_user.id
    
    current_state = await state.get_state()
    if current_state == 'ChangeNoteStates:WAITING_NEW_TEXT':
        await get_new_text(callback_query.message, state)
    elif current_state == 'ChangeNoteStates:WAITING_NEW_TIME':
        await get_new_time(callback_query.message, state)
    else:
        logger.error(f'The logic of work is broken. Unexpected state: {current_state}')