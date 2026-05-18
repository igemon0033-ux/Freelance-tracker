import requests
import os
from base.db import Database

import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    texts = settings["texts"]
    token = settings["token"]

# Прокси из настроек
PROXY_URL = "http://W5wUKarZ:9FzWg75k@142.111.3.115:63360"
proxies = {
    "http": PROXY_URL,
    "https": PROXY_URL
}

def send_project(category: str, site_name: str, price: int, number_of_responses: int, task_description: str,
                       link: str, project_id: str = None, project_name: str = ""):
    BaseClass = Database()

    # Get users who are interested in this category
    users = BaseClass.get_users_by_order(category, site_name)

    if len(task_description) > 400:
        task_description = task_description[0:400] + "......"
        
    message_text = texts["project_text"].format(
        site_name, category, price, number_of_responses, task_description
    )

    # Формируем клавиатуру
    buttons = [
        {"text": "🔗 Посмотреть заказ", "url": link}
    ]
    
    if project_id:
        buttons.append({"text": "🤖 Сгенерировать отклик", "callback_data": f"ai_draft:{project_id}"})

    reply_markup = {
        "inline_keyboard": [buttons]
    }


    for user in users:
        # Сохраняем описание проекта для ИИ (если переданы данные)
        if project_id:
            try:
                projects_file = "freelance_orders/projects.json"
                projects_data = {}
                if os.path.exists(projects_file):
                    with open(projects_file, "r", encoding="utf-8") as f:
                        projects_data = json.load(f)
                
                projects_data[project_id] = {
                    "name": project_name,
                    "description": task_description,
                    "category": category,
                    "price": price
                }
                
                # Храним только последние 100 проектов
                if len(projects_data) > 100:
                    keys = list(projects_data.keys())
                    del projects_data[keys[0]]

                with open(projects_file, "w", encoding="utf-8") as f:
                    json.dump(projects_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error saving project data: {e}")

        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"

            payload = {
                "chat_id": user,
                "text": message_text,
                "reply_markup": json.dumps(reply_markup),
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=payload, proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                if not BaseClass.get_user_active(user):
                    BaseClass.change_user_active(user)
            else:
                print(f"Error sending message to {user}: {response.text}")
                
        except Exception as e:
            print(f"Error sending message to {user}: {e}")
