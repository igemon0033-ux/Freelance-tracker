from globals import dp, channels, texts, bot, main_keyboard, admins
from utils.subscribe_check import check
from aiogram import types
from base.db import Database
from parsers.send_project import send_project


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id in admins:
        BaseClass = Database()
        # BaseClass.svod()
        stats = BaseClass.get_users_stats()
        # print(stats)
        await bot.send_message(message.chat.id, f"Нажали старт: {stats['users']}\n"
                                                f"Подписались на уведомления: {stats['active_users']}\n"
                                                f"Получают уведомления: {stats['real_users']}")
