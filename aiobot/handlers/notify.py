from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import bot, dp, pg
from keyboards.notes import notify_note_kbrd, new_time_kbrd
from keyboards.buttons import return_kbrd


class ChangeTimeState(StatesGroup):
    WAITING_NEW_TIME = State()
    

async def notify(user_id: int, note_id: int, note_title: str, note_text: str):  
    kbrd = await notify_note_kbrd(note_id)
    
    await bot.send_message(
        chat_id=user_id, 
        text=f'Пришло время напомнить:\n\n*{note_title}*\n{note_text}',
        reply_markup=kbrd,
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('complete'))
async def complete_note_call(callback_query: CallbackQuery):
    await callback_query.answer()
    await complete_note(callback_query)
    
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('complete'), state='*')
async def complete_note_state(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.finish()
    
    await complete_note(callback_query)

async def complete_note(callback_query: CallbackQuery):  
    query = """ UPDATE notes SET reminder_time = NULL WHERE id = $1; """
    note_id = int(callback_query.data[8:])
    await pg.execute(query, note_id, execute=True)
    
    await callback_query.message.answer(
        text='Заметка выполнена, но не удалена',
        reply_markup=return_kbrd
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('newtime'))
async def handle_every_note(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
        
    note_id = int(callback_query.data[7:])
    await state.update_data(note_id=note_id)
    
    kbrd = await new_time_kbrd(note_id)
    
    await callback_query.message.answer(
        text='Введи новое время для напоминания в формате "дд.мм.гггг чч:мм"',
        reply_markup=kbrd
    )
    
    await state.set_state(ChangeTimeState.WAITING_NEW_TIME)


@dp.message_handler(state=ChangeTimeState.WAITING_NEW_TIME)
async def get_new_time(message: Message, state: FSMContext):
    note_time = message.text
    
    data = await state.get_data()
    note_id = data.get('note_id')
    
    kbrd = await new_time_kbrd(note_id)
    
    if note_time:
        try:
            note_time = datetime.strptime(note_time, '%d.%m.%Y %H:%M')
            
            if note_time <= datetime.now():
                await message.answer(
                    text='Это время выбрать невозможно, оно уже прошло...',
                    reply_markup=kbrd
                )
                return
        except ValueError:
            await message.answer(
                text='Неверный формат даты и времени :( Попробуй еще раз',
                reply_markup=kbrd
            )
    
    query = """ UPDATE notes SET reminder_time = $1 WHERE id = $2; """
    await pg.execute(query, note_time, note_id, execute=True)
        
    await message.answer(
        text='Заметка успешно обновлена!',
        reply_markup=return_kbrd
    )
    await state.finish()