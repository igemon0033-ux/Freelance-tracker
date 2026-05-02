from globals import dp, texts, bot, min_budget
from aiogram import types
from base.db import Database


@dp.callback_query_handler(text="choose_kwork_budget")
async def without_puree(call: types.CallbackQuery):
    usid = call.from_user.id

    BaseClass = Database()

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
