from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""
Инлайн клавиатура для выбора часового пояса
"""

time_zone_kbrd = InlineKeyboardMarkup(
    # часовые пояса не все, но, впринципе, хватило бы и одного
    inline_keyboard=[
        [
            InlineKeyboardButton(text='-11:00', callback_data='tz-11'),
            InlineKeyboardButton(text='-10:00', callback_data='tz-1'),
            InlineKeyboardButton(text='-9:00', callback_data='tz-9'),
            InlineKeyboardButton(text='-8:00', callback_data='tz-8'),
            InlineKeyboardButton(text='-7:00', callback_data='tz-7'),
            InlineKeyboardButton(text='-6:00', callback_data='tz-6'),
        ],
        [
            InlineKeyboardButton(text='-5:00', callback_data='tz-5'),
            InlineKeyboardButton(text='-4:00', callback_data='tz-4'),
            InlineKeyboardButton(text='-3:00', callback_data='tz-3'),
            InlineKeyboardButton(text='-2:00', callback_data='tz-2'),
            InlineKeyboardButton(text='-1:00', callback_data='tz-1'),
            InlineKeyboardButton(text='-0:00', callback_data='tz-0'),
        ],
        [
            InlineKeyboardButton(text='+1:00', callback_data='tz+1'),
            InlineKeyboardButton(text='+2:00', callback_data='tz+2'),
            InlineKeyboardButton(text='+3:00', callback_data='tz+3'),
            InlineKeyboardButton(text='+4:00', callback_data='tz+4'),
            InlineKeyboardButton(text='+5:00', callback_data='tz+5'),
            InlineKeyboardButton(text='+6:00', callback_data='tz+6'),
        ],
        [
            InlineKeyboardButton(text='+7:00', callback_data='tz+7'),
            InlineKeyboardButton(text='+8:00', callback_data='tz+8'),
            InlineKeyboardButton(text='+9:00', callback_data='tz+9'),
            InlineKeyboardButton(text='+10:00', callback_data='tz+1'),
            InlineKeyboardButton(text='+11:00', callback_data='tz+11'),
            InlineKeyboardButton(text='+12:00', callback_data='tz+12'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_call'),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)