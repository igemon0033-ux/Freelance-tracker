import google.generativeai as genai
import json
import os
from utils.portfolio_context import PORTFOLIO_CONTEXT

def generate_pitch(project_name, project_description):
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            api_key = settings.get("gemini_key")
        
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            return "⚠️ Ошибка: В settings.json не указан рабочий 'gemini_key'. Пожалуйста, замени 'YOUR_GEMINI_API_KEY_HERE' на свой реальный API-ключ Gemini."

        # Настройка прокси для обхода блокировок Google API в РФ
        PROXY_URL = "http://W5wUKarZ:9FzWg75k@142.111.3.115:63360"
        os.environ["HTTP_PROXY"] = PROXY_URL
        os.environ["HTTPS_PROXY"] = PROXY_URL

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
