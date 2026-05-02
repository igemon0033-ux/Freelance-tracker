from aiogram import types
import aiogram
from globals import dp, texts, bot, main_keyboard, exchanges, categories
from base.db import Database
from utils.get_dict_keys import get_keys, get_leaf_values, find_path
import json
from utils.dict_search import find_key_in_nested_dict


@dp.callback_query_handler(text=list(categories.keys()))
async def rubrics_change(call: types.CallbackQuery):
    # print(get_keys(categories, 2))
    # print(call.data)
    usid = call.from_user.id
    categories_list = find_key_in_nested_dict(categories, call.data)

    buttons = []

    BaseClass = Database()
    user_rubrics = BaseClass.get_user_categories(usid)

    for elem in categories_list:
        buttons.append(
            types.InlineKeyboardButton(text=f"{'✅' if elem in user_rubrics else ''}{elem}", callback_data=elem))
    # w = find_path(categories, call.data)[0]
    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="category_change"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    try:
        await call.message.edit_text(text=texts["choose_categories"], reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
