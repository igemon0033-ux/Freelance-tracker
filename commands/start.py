from globals import dp, channels, texts, bot, main_keyboard
from utils.subscribe_check import check
from aiogram import types
from base.db import Database
from parsers.send_project import send_project


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    Flag = False

    BaseClass = Database()
    BaseClass.add_user(user_id)

    for chanel in channels:
        # subscribed = await check(chanel[1], user_id)
        try:
            user_channel_status = await bot.get_chat_member(chat_id=chanel[1], user_id=user_id)
            if user_channel_status["status"] != 'left':
                subscribed = 1
            else:
                subscribed = 0
        except Exception as ex:
            print(user_id)
            print(ex)
            subscribed = 2

        if subscribed == 0:
            buttons = []
            for i in range(len(channels)):
                buttons.append(types.InlineKeyboardButton(text=f"Подписаться!", url=channels[i][0]))
            buttons.append(types.InlineKeyboardButton(text="Я уже подписан!", callback_data="subscribed"))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await bot.send_message(message.chat.id, texts["subcribe_pls_text"], reply_markup=keyboard, parse_mode="HTML")
            Flag = True
            break
    if not Flag:
        await bot.send_message(message.chat.id, texts["start_text"], reply_markup=main_keyboard)
