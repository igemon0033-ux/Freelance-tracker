import json

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    texts = settings["texts"]
    channels = settings["channels"]
    exchanges = settings["exchanges"]
    categories = settings["categories"]
    admins = settings["admins"]
    min_budget = settings["min_budget"]
    # print(list(categories.keys()))

storage = MemoryStorage()

# Используем ваш личный прокси из настроек Telegram
PROXY_URL = "http://W5wUKarZ:9FzWg75k@142.111.3.115:63360" 
bot = Bot(settings["token"], proxy=PROXY_URL, parse_mode="HTML") 
dp = Dispatcher(bot, storage=storage)

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add('⚙️Настройки', 'ℹ️ Информация')
