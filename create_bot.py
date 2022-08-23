from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from token_tg import token 

storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)