from globals import dp, texts, bot, min_budget
from aiogram import types


@dp.callback_query_handler(text=["back_to_settings"])
async def without_puree(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="✏️Изменить категории", callback_data="category_change"),
               types.InlineKeyboardButton(text="📋Выбрать биржи", callback_data="choose_exchange"),
               types.InlineKeyboardButton(text="💰Установить бюджет заказов с kwork",
                                          callback_data="choose_kwork_budget")
               #    types.InlineKeyboardButton(text="🔔Настройки уведомлений", callback_data="notification_settings")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(text=texts["settings_text"], reply_markup=keyboard)
