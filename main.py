import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters.command import Command
from decouple import config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random


bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
bot_router = Router()


class Step(StatesGroup):
    guesses = State()
    finish = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Начнём игру. Я загадал число от 1 до 100 (1 тоже может быть, и 100 тоже может быть). Число целое. Попробуй угадать какое за наименьшее количество попыток.")
    await state.set_state(Step.guesses)
    the_number = random.randint(1, 100)
    await state.update_data(the_number=the_number)
    await state.update_data(attempt=0)


@dp.message(Step.guesses)
async def ask(message: Message, state: FSMContext):
    storage_data = await state.get_data()
    attempt = int(storage_data.get('attempt', 0))
    the_number = int(storage_data.get('the_number'))
    attempt = attempt + 1

    await state.update_data(attempt=attempt)
    try:
        a_number = int(message.text)
        if a_number == the_number:
            await message.answer('Молодец, ты отгадал!')
            await message.answer(f'За {attempt} попыток')
        else:
            # не отгадал. дадим подсказку
            if the_number > a_number:
                await message.answer('Загаданное число больше')
            else:
                await message.answer('Загаданное число меньше')
    except Exception as e:
        await message.answer('Это не число')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
