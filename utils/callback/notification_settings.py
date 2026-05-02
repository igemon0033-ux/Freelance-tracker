from aiogram import types
from globals import dp, texts, bot, main_keyboard
from base.db import Database
import json


@dp.callback_query_handler(text=["notification_settings"])
async def add_exchange(call: types.CallbackQuery):
    # print(1)
    usid = call.from_user.id
    BaseClass = Database()
    user_exchanges = BaseClass.get_user_notifications(usid)

    buttons = []
    if user_exchanges:
        buttons.append(types.InlineKeyboardButton(text="Выключить уведомления", callback_data="change_notification"))
    else:
        buttons.append(types.InlineKeyboardButton(text="Включить уведомления", callback_data="change_notification"))

    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="back_to_settings"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.edit_text(text=texts["notification_text"], reply_markup=keyboard)
