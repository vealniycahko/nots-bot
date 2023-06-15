from asyncpg import Record
from typing import List
from datetime import timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


"""
Специальные инлайн клавиатуры,
которые генерируют коллбэки с айдишниками заметок для дальнейшей их обработки
"""


async def notes_inline_kbrd(notes: List[Record], tz: int) -> InlineKeyboardMarkup:
    notes_kbrd = InlineKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    for row in notes:
        if row['reminder_time']:
            reminder_time = row['reminder_time'] + timedelta(hours=int(tz))
            text = f'{row["note_title"]} {reminder_time.strftime("%d.%m.%Y %H:%M")}'
        else:
            text = f'{row["note_title"]}'
        callback = f'open{row["id"]}'
        button = InlineKeyboardButton(text=text, callback_data=callback)
        notes_kbrd.add(button)
        
    notes_kbrd.add(
        InlineKeyboardButton(text='Вернуться', callback_data='start_call'),
        InlineKeyboardButton(text='Создать заметку', callback_data='create_call')
    )
        
    return notes_kbrd


async def single_note_kbrd(note_id: str) -> InlineKeyboardMarkup:
    note_kbrd = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить', callback_data=f'change{note_id}'),
                InlineKeyboardButton(text='Удалить', callback_data=f'delete{note_id}'),
            ],
            [
                InlineKeyboardButton(text='Мои заметки', callback_data='notes_call'),
                InlineKeyboardButton(text='Отмена', callback_data='start_call'),
            ],
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    return note_kbrd


async def notify_note_kbrd(note_id: str) -> InlineKeyboardMarkup:
    kbrd = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Готово', callback_data=f'complete{note_id}'),
                InlineKeyboardButton(text='Новое время', callback_data=f'newtime{note_id}'),
                InlineKeyboardButton(text='Удалить', callback_data=f'delete{note_id}'),
            ],
            [
                InlineKeyboardButton(text='Мои заметки', callback_data='notes_call'),
            ],
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    return kbrd


async def new_time_kbrd(note_id: str) -> InlineKeyboardMarkup:
    kbrd = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Готово', callback_data=f'complete{note_id}'),
                InlineKeyboardButton(text='Удалить заметку', callback_data=f'delete{note_id}'),
                InlineKeyboardButton(text='Отмена', callback_data='cancel_call'),
            ],
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    return kbrd