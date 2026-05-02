from aiogram import types
import aiogram
from globals import dp, texts, bot, main_keyboard, exchanges, categories
from base.db import Database
import json


@dp.callback_query_handler(text=["category_change"])
async def category_change(call: types.CallbackQuery):
    categories_list = list(categories.keys())
    buttons = []

    for elem in categories_list:
        buttons.append(types.InlineKeyboardButton(text=elem, callback_data=elem))
    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="back_to_settings"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    try:
        await call.message.edit_text(text=texts["choose_categories"], reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
