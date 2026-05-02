from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
from base.db import Database
from globals import channels
from utils.subscribe_check import check

with open("settings.json", "r", encoding="utf 8") as f:
    settings = json.load(f)
    texts = settings["texts"]

bot = Bot(settings["token"], parse_mode="HTML")


async def send_project(category: str, site_name: str, price: int, number_of_responses: int, task_description: str,
                       link: str):
    BaseClass = Database()

    if "kwork" in link:
        link += "?ref=12561466"

    users = BaseClass.get_users_by_order(category, site_name)

    if len(task_description) > 200:
        task_description = task_description[0:200] + "......"
    message_text = texts["project_text"].format(
        site_name, category, price, number_of_responses, task_description
    )

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="🔗 Посмотреть заказ", url=link))

    for user in users:
        kwork_budget = BaseClass.get_user_kwork_budget(user)
        Flag = False
        if price > kwork_budget:
            for chanel in channels:
                # subscribed = await check(chanel[1], user)

                try:
                    user_channel_status = await bot.get_chat_member(chat_id=chanel[1], user_id=user)
                    if user_channel_status["status"] != 'left':
                        subscribed = 1
                    else:
                        subscribed = 0
                except Exception as ex:
                    print(user)
                    print(ex)
                    subscribed = 2

                if subscribed == 0:

                    buttons = []
                    for i in range(len(channels)):
                        buttons.append(InlineKeyboardButton(text=f"Канал {i + 1}", url=channels[i][0]))
                    buttons.append(InlineKeyboardButton(text="Я подписался", callback_data="subscribed"))
                    keyboard = InlineKeyboardMarkup(row_width=1)
                    keyboard.add(*buttons)
                    try:
                        await bot.send_message(user, texts["project_subscribe_text"], reply_markup=keyboard)
                        if BaseClass.get_user_active(user):
                            BaseClass.change_user_active(user)
                    except:
                        if not BaseClass.get_user_active(user):
                            BaseClass.change_user_active(user)
                    Flag = True
                    break
            if not Flag:
                try:
                    await bot.send_message(user, message_text, reply_markup=kb)

                    if not BaseClass.get_user_active(user):
                        BaseClass.change_user_active(user)
                except:
                    if BaseClass.get_user_active(user):
                        BaseClass.change_user_active(user)
