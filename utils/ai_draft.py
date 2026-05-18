import google.generativeai as genai
import json
from utils.portfolio_context import PORTFOLIO_CONTEXT

def generate_pitch(project_name, project_description):
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            api_key = settings.get("gemini_key")
        
        if not api_key:
            return "⚠️ Ошибка: В settings.json не указан 'gemini_key'. Пожалуйста, добавь свой API ключ Gemini."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
{PORTFOLIO_CONTEXT}

ЗАКАЗ:
Название: {project_name}
Описание: {project_description}

Напиши идеальный отклик для этого заказа. Отклик должен быть лаконичным (не более 600 символов), показывать понимание задачи и предлагать решение. Обязательно упомяни релевантный опыт (если задача про парсинг — про Arlight/Blesslight).
"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Ошибка при генерации отклика: {str(e)}"
