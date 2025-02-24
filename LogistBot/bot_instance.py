from aiogram import Bot, Dispatcher

import config

API_TOKEN = config.BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()