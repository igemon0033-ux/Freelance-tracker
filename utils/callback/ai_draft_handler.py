from globals import dp, bot
from aiogram import types
import json
import os
from utils.ai_draft import generate_pitch

@dp.callback_query_handler(lambda c: c.data.startswith('ai_draft:'))
async def ai_draft_callback(callback_query: types.CallbackQuery):
    project_id = callback_query.data.split(':')[1]
    
    await bot.answer_callback_query(callback_query.id, text="Генерирую отклик... 🤖")
    
    # Загружаем данные проекта
    projects_file = "freelance_orders/projects.json"
    project_data = None
    
    if os.path.exists(projects_file):
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)
            project_data = projects.get(project_id)
            
    if not project_data:
        await bot.send_message(callback_query.from_user.id, "❌ Извините, данные проекта не найдены.")
        return

    # Генерируем отклик
    pitch = generate_pitch(project_data['name'], project_data['description'])
    
    response_text = f"🤖 <b>Вариант отклика для заказа:</b>\n\n<code>{pitch}</code>\n\n<i>Скопируйте текст и отправьте его заказчику.</i>"
    
    await bot.send_message(callback_query.from_user.id, response_text, parse_mode="HTML")
