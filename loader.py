from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import config


token = "766788460:AAFE1HybmKkPgsEdQGgEGZYIMnHca6B0iRk"
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)#config.config("bot_token"), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
vip = Dispatcher(bot, storage=storage)
