from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


skip_cancel_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='skip_data'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


cancel_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


start_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать заметку', callback_data='1'),
        ],
        [
            InlineKeyboardButton(text='Мои заметки', callback_data='2')
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
