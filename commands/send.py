from globals import dp, channels, texts, bot, main_keyboard, admins
from utils.subscribe_check import check
from aiogram import types
from base.db import Database
from parsers.send_project import send_project


@dp.message_handler(commands=['send'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id in admins:
        args = message.get_args()
        if args is not None:
            send_text = "".join(args)
        else:
            await bot.send_message(message.chat.id, "Неверный текст")
            return
        BaseClass = Database()
        users = BaseClass.get_all_users()
        for user in users:
            try:
                if not user in admins:
                    await bot.send_message(user, send_text)
                    if not BaseClass.get_user_active(user):
                        BaseClass.change_user_active(user)
            except:
                if BaseClass.get_user_active(user):
                    BaseClass.change_user_active(user)
