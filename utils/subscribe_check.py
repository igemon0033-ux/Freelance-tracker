from globals import bot
import json

with open("settings.json", "r", encoding="utf 8") as f:
    settings = json.load(f)


async def check(chat_check_id, check_user_id):
    try:
        user_channel_status = await bot.get_chat_member(chat_id=chat_check_id, user_id=check_user_id)
        if user_channel_status["status"] != 'left':
            return 1
        else:
            return 0
    except Exception as ex:
        print(ex)
        return 2
