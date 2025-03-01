from aiogram import Bot, Dispatcher, types
from aiogram import Router
from decouple import config
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
bot_router = Router()
