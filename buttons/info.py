from globals import dp, texts, bot
from aiogram import types


@dp.message_handler(lambda message: message.text == "ℹ️ Информация")
async def without_puree(message: types.Message):
    await bot.send_message(message.chat.id, texts["info_button"])
