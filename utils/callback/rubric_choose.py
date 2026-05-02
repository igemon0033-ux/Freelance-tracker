from aiogram import types
import aiogram
from globals import dp, texts, bot, categories, categories
from base.db import Database
from utils.get_dict_keys import get_keys, get_leaf_values, find_path
from utils.dict_search import find_key_in_nested_dict, find_key_or_value_in_nested_dict
import json


@dp.callback_query_handler(text=sum(get_leaf_values(categories), []))
async def change_rubric(call: types.CallbackQuery):
    usid = call.from_user.id
    BaseClass = Database()
    user_categories = BaseClass.get_user_categories(usid)
    category_name = call.data
    categories_list = find_key_or_value_in_nested_dict(categories, call.data)
    if category_name in user_categories:
        user_categories.remove(category_name)
    else:
        user_categories.append(category_name)

    # print(user_categories)

    BaseClass.change_user_categories(usid, user_categories)

    buttons = []

    for elem in categories_list:
        if elem in user_categories:
            buttons.append(types.InlineKeyboardButton(text=f"✅{elem}", callback_data=elem))
        else:
            buttons.append(types.InlineKeyboardButton(text=f"{elem}", callback_data=elem))
    w = find_path(categories, call.data)
    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="category_change"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    try:
        await call.message.edit_text(text=texts["choose_categories"], reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
