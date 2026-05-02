from globals import dp, texts, bot
from aiogram import types


@dp.message_handler(lambda message: message.text == "⚙️Настройки")
async def without_puree(message: types.Message):
    buttons = [types.InlineKeyboardButton(text="✏️Изменить категории", callback_data="category_change"),
               types.InlineKeyboardButton(text="📋Выбрать биржи", callback_data="choose_exchange"),
               types.InlineKeyboardButton(text="💰Установить бюджет заказов с kwork", callback_data="choose_kwork_budget")
               #    types.InlineKeyboardButton(text="🔔Настройки уведомлений", callback_data="notification_settings")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, texts["settings_text"], reply_markup=keyboard)
