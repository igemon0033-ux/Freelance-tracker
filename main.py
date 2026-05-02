from aiogram import executor as ex
from commands import start, info, send
from utils.callback import exchange_choose
from buttons import settings, info, off_ads
from utils.callback import settings_page
from utils.callback import subscribed
from utils.callback import exchange_choose
from utils.callback import exchange_settings
from utils.callback import turn_notifications
from utils.callback import notification_settings
from utils.callback import categories_button
# from utils.callback import subcategories_button
from utils.callback import rubrics_buttons
# from utils.callback import prerubric_choose
from utils.callback import rubric_choose
from utils.callback import choose_kwork_budget_callback, choose_kwork_budget_button
from globals import dp, channels, texts, bot, main_keyboard, categories
from utils.get_dict_keys import get_keys
from threading import Thread
import json

import parsers.kwork as kwork_parser

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)


def start_parsers():
    Thread(target=kwork_parser.run).start()


async def bot_callback(x):
    print("Started")


if __name__ == '__main__':
    start_parsers()
    ex.start_polling(dp, on_startup=bot_callback)
