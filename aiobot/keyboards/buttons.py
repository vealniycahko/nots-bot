from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


skip_cancel_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='skip_data_call'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_call'),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


cancel_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_call'),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


start_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать заметку', callback_data='create_call'),
            InlineKeyboardButton(text='Мои заметки', callback_data='notes_call')
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


create_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать заметку', callback_data='create_call'),
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


return_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Мои заметки', callback_data='notes_call'),
            InlineKeyboardButton(text='Вернуться', callback_data='start_call'),
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


skip_update_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='skip_update_call'),
            InlineKeyboardButton(text='Отмена', callback_data='notes_call'),
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


skip_clean_update_kbrd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='skip_update_call'),
            InlineKeyboardButton(text='Очистить', callback_data='clean_update_call'),
            InlineKeyboardButton(text='Отмена', callback_data='notes_call'),
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
