from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import bot, dp, rd, pg
from keyboards.notes import notify_note_kbrd, new_time_kbrd
from keyboards.buttons import return_kbrd
from keyboards.timezone import time_zone_kbrd
from utils import emoji


"""
Уведомление пользовалей:

Отправка сообщений при наступлении времени напоминания (это происходит в sheduler)
Выполнение заметки (удаление времени напоминания)
Обновление времени напоминания
"""


class ChangeTimeState(StatesGroup):
    WAITING_NEW_TIME = State()
    WAITING_TZ = State()


async def notify(user_id: int, note_id: str, note_title: str, note_text: str):
    """
    Функция запускается, когда sheduler обнаруживает заметку,
    у которой наступило время напоминания
    """
    kbrd = await notify_note_kbrd(note_id)

    await bot.send_message(
        chat_id=user_id,
        text=f"{emoji.bell} Пришло время напомнить:\n\n*{note_title}*\n{note_text}",
        reply_markup=kbrd,
        parse_mode="Markdown",
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("complete")
)
async def complete_note_call(callback_query: CallbackQuery):
    await callback_query.answer()
    await complete_note(callback_query)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("complete"), state="*"
)
async def complete_note_state(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.finish()
    await complete_note(callback_query)


async def complete_note(callback_query: CallbackQuery):
    query = """ UPDATE notes SET reminder_time = NULL WHERE id = $1; """
    note_id = callback_query.data[8:]
    await pg.execute(query, note_id, execute=True)

    await callback_query.message.answer(
        text=f"{emoji.checkmark} Заметка выполнена, но не удалена",
        reply_markup=return_kbrd,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("newtime")
)
async def handle_every_note(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    note_id = callback_query.data[7:]
    await state.update_data(note_id=note_id)

    kbrd = await new_time_kbrd(note_id)

    await callback_query.message.answer(
        text=f'{emoji.pushpin} Введи новое время для напоминания в формате "дд.мм.гггг чч:мм"',
        reply_markup=kbrd,
    )

    await state.set_state(ChangeTimeState.WAITING_NEW_TIME)


@dp.message_handler(state=ChangeTimeState.WAITING_NEW_TIME)
async def get_new_time(message: Message, state: FSMContext):
    note_time = message.text
    await state.update_data(new_time=note_time)

    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    data = await state.get_data()
    note_id = data.get("note_id")

    kbrd = await new_time_kbrd(note_id)

    if note_time:
        try:
            note_time = datetime.strptime(note_time, "%d.%m.%Y %H:%M")
        except ValueError:
            await message.answer(
                text=f"{emoji.exclaim} Неверный формат даты и времени... Попробуй еще раз",
                reply_markup=kbrd,
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
                text=f"{emoji.pushpin} Выбери свой часовой пояс в формате UTC(ты сможешь его изменить)\n\
                    Часовой пояс Москвы по UTC - +3:00 и так далее",
                reply_markup=time_zone_kbrd,
            )
            await state.set_state(ChangeTimeState.WAITING_TZ)
    else:
        await complete_updating(message, state)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("tz"),
    state=ChangeTimeState.WAITING_TZ,
)
async def get_time_zone(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    data = await state.get_data()
    user_id = data.get("user_id")
    note_time = data.get("new_time")

    tz = int(callback_query.data[2:])
    await rd.set_tz(user_id, tz)

    offset = timedelta(hours=tz)
    note_time = note_time - offset
    await state.update_data(new_time=note_time)
    await complete_updating(callback_query.message, state)


async def complete_updating(message: Message, state: FSMContext):
    data = await state.get_data()

    note_time = data.get("new_time")
    note_id = data.get("note_id")

    query = """ UPDATE notes SET reminder_time = $1 WHERE id = $2; """
    await pg.execute(query, note_time, note_id, execute=True)

    await message.answer(
        text=f"{emoji.checkmark} Заметка успешно обновлена!", reply_markup=return_kbrd
    )

    await state.finish()
