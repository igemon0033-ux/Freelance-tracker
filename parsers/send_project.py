from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from base.db import Database

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    texts = settings["texts"]

bot = Bot(settings["token"], parse_mode="HTML")


async def send_project(category: str, site_name: str, price: int, number_of_responses: int, task_description: str,
                       link: str):
    BaseClass = Database()

    # Get users who are interested in this category
    users = BaseClass.get_users_by_order(category, site_name)

    if len(task_description) > 400:
        task_description = task_description[0:400] + "......"
        
    message_text = texts["project_text"].format(
        site_name, category, price, number_of_responses, task_description
    )

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="🔗 Посмотреть заказ", url=link))

    for user in users:
        try:
            # For personal use, we send the project directly without subscription checks
            await bot.send_message(user, message_text, reply_markup=kb)
            
            if not BaseClass.get_user_active(user):
                BaseClass.change_user_active(user)
        except Exception as e:
            print(f"Error sending message to {user}: {e}")
            if BaseClass.get_user_active(user):
                BaseClass.change_user_active(user)
