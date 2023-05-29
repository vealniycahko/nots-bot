# from aiogram.types import Message
# from aiogram.dispatcher.filters import CommandStart, Command
# from aiogram.dispatcher import FSMContext

# from aiogram import __main__ as core
# from core.main import dp


# class CreateNoteStates(types.states.Group):
#     WAITING_TITLE = types.State()


# @dp.message_handler(Command('create'))
# async def start_create_command(message: Message):
#     await message.answer('Название заметки введи ну-ка')

#     await CreateNoteStates.WAITING_TITLE.set()


# @dp.message_handler(state=CreateNoteStates.WAITING_TITLE)
# async def process_note_title(message: Message, state: FSMContext):
#     note_title = message.text
#     await state.finish()
#     await message.answer(f'Заметка "{note_title}" создана!')
