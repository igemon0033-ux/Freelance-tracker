from aiogram import types
import aiogram
from globals import dp, texts, min_budget
from base.db import Database
from utils.get_dict_keys import get_keys, get_leaf_values, find_path
from utils.dict_search import find_key_in_nested_dict, find_key_or_value_in_nested_dict
import json


@dp.callback_query_handler(lambda call: "set_kwork_budget_" in call.data)
async def change_rubric(call: types.CallbackQuery):
    usid = call.from_user.id
    BaseClass = Database()

    budget = call.data[len("set_kwork_budget_"):]
    BaseClass.change_user_kwork_budget(usid, budget)

    user_budget = BaseClass.get_user_kwork_budget(usid)

    buttons = []

    for elem in min_budget:
        if elem == user_budget:
            buttons.append(types.InlineKeyboardButton(text=f"✅{elem}₽", callback_data=f"set_kwork_budget_{elem}"))
        else:
            buttons.append(types.InlineKeyboardButton(text=f"{elem}₽", callback_data=f"set_kwork_budget_{elem}"))

    buttons.append(types.InlineKeyboardButton(text="Назад", callback_data="back_to_settings"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.edit_text(text=texts["choose_kwork_budget"], reply_markup=keyboard)
