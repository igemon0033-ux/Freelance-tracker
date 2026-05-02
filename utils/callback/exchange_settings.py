import json

from aiogram import types
from utils.subscribe_check import check
from globals import dp, texts, bot, main_keyboard, exchanges
from buttons import settings
from base.db import Database


@dp.callback_query_handler(text=["choose_exchange"])
async def add_exchange(call: types.CallbackQuery):
    usid = call.from_user.id
    BaseClass = Database()
    user_exchanges = BaseClass.get_user_exchanges(usid)

    buttons = []

    for elem in exchanges:
        if elem in user_exchanges:
            buttons.append(types.InlineKeyboardButton(text=f"✅{elem}", callback_data=elem))
        else:
            buttons.append(types.InlineKeyboardButton(text=f"{elem}", callback_data=elem))

    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="back_to_settings"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.edit_text(text=texts["choose_exchange_button"], reply_markup=keyboard)
