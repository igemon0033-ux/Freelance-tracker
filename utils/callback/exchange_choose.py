from aiogram import types
import aiogram
from globals import dp, texts, bot, main_keyboard, exchanges
from base.db import Database
from utils.get_dict_keys import get_keys
import json


@dp.callback_query_handler(text=exchanges)
async def add_exchange(call: types.CallbackQuery):
    usid = call.from_user.id
    BaseClass = Database()
    user_exchanges = BaseClass.get_user_exchanges(usid)
    ex_name = call.data
    if ex_name in user_exchanges:
        user_exchanges.remove(ex_name)
    else:
        user_exchanges.append(ex_name)

    BaseClass.change_user_exchanges(usid, json.dumps(user_exchanges))

    buttons = []

    for elem in exchanges:
        if elem in user_exchanges:
            buttons.append(types.InlineKeyboardButton(text=f"✅{elem}", callback_data=elem))
        else:
            buttons.append(types.InlineKeyboardButton(text=f"{elem}", callback_data=elem))

    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="back_to_settings"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    try:
        await call.message.edit_text(text=texts["choose_exchange_button"], reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
