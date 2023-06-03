import config

import webbrowser

from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class InputState(StatesGroup):
    input = State()

storage = MemoryStorage()
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}\n"
                         "Введите артикул")
    await InputState.input.set()

@dp.message_handler(commands=["stop"], state='*')
async def stop(message: types.Message, state: FSMContext):
    await message.answer("Бот завершил работу")
    await state.finish()
    
@dp.message_handler(state=InputState.input)
async def inp_art(message: types.Message, state: FSMContext):
    url = f"https://www.wildberries.ru/catalog/{message.text}/detail.aspx"
    if message.text.isdigit():
        webbrowser.open(url)
        await message.reply(url)
    else:
        await message.reply("Неверный артикул")



executor.start_polling(dp)