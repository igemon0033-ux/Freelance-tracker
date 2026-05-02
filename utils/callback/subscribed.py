from aiogram import types
from utils.subscribe_check import check
from globals import dp, channels, texts, bot, main_keyboard


@dp.callback_query_handler(text="subscribed")
async def check_subscribe(call: types.CallbackQuery):
    usid = call.from_user.id
    Flag = False
    for chanel in channels:
        # subscribed = await check(chanel[1], usid)

        try:
            user_channel_status = await bot.get_chat_member(chat_id=chanel[1], user_id=usid)
            if user_channel_status["status"] != 'left':
                subscribed = 1
            else:
                subscribed = 0
        except Exception as ex:
            print(usid)
            print(ex)
            subscribed = 2

        if subscribed == 0:
            buttons = []
            for i in range(len(channels)):
                buttons.append(types.InlineKeyboardButton(text=f"Подписаться!", url=channels[i][0]))
            buttons.append(types.InlineKeyboardButton(text="Я подписался", callback_data="subscribed"))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await bot.send_message(call.message.chat.id, texts["subcribe_pls_text"], reply_markup=keyboard, parse_mode="HTML")
            Flag = True
            break
    if not Flag:
        await bot.send_message(call.message.chat.id, texts["start_text"], reply_markup=main_keyboard, parse_mode="HTML")
