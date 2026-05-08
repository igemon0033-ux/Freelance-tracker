import requests
import re
import asyncio
import json
import logging
from parsers.send_project import send_project

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SITE_NAME = "kwork"
SITE_URL = "https://kwork.ru/projects"

# Наши ключевые слова для фильтрации (в нижнем регистре)
KEYWORDS = [
    "python", "телеграм", "бот", "парсер", "автоматизация", 
    "авито", "excel", "таблицы", "скрипт", "ai", "ии", 
    "чат-бот", "парсинг", "выгрузка", "автоответчик"
]

MIN_BUDGET = 500  # Минимальный бюджет для уведомления
PRIORITY_BUDGET = 3000  # Бюджет, который мы считаем приоритетным (жирным)

with open("cats.json", "r", encoding="utf-8") as f:
    cats = json.load(f)

def contains_keywords(text):
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in KEYWORDS)

async def main():
    # Загружаем уже виденные ID из файла, чтобы не дублировать после перезагрузки
    ignore_ids = []
    try:
        with open("seen_ids.txt", "r") as f:
            ignore_ids = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        pass

    first_run = True
    logging.info(f"Мониторинг Kwork запущен. В базе уже {len(ignore_ids)} просмотренных проектов.")

    while True:
        try:
            # Используем сессию для эффективности
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(SITE_URL, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logging.error(f"Ошибка доступа к сайту: {response.status_code}")
                await asyncio.sleep(10)
                continue

            # Извлекаем данные из window.stateData
            match = re.search(r"window\.stateData=(.*?)};", response.text)
            if not match:
                logging.error("Не удалось найти stateData на странице")
                await asyncio.sleep(10)
                continue

            data_str = match.group(1) + "}"
            data = json.loads(data_str)
            wants_list = data.get("wantsListData", {}).get("wants", [])

            for want in wants_list:
                id_ = str(want["id"])
                name = want.get("name", "")
                description = want.get("description", "")
                number_of_responses = want.get("kwork_count", 0)
                category_id = str(want.get("category_id", ""))
                category = cats.get(category_id, "Без категории")
                price_limit = round(float(want.get("priceLimit", 0)))

                # Пропускаем уже виденные проекты
                if id_ in ignore_ids:
                    continue
                
                ignore_ids.append(id_)
                # Сразу записываем в файл, чтобы не потерять при падении
                with open("seen_ids.txt", "a") as f:
                    f.write(f"{id_}\n")
                
                # ФИЛЬТРАЦИЯ
                is_relevant = contains_keywords(name) or contains_keywords(description)
                is_good_budget = price_limit >= MIN_BUDGET
                
                # Если проект интересен по ключевым словам ИЛИ имеет высокий бюджет
                if (is_relevant and is_good_budget) or price_limit >= PRIORITY_BUDGET:
                    logging.info(f"Найдено совпадение! {name} ({price_limit} руб.)")
                    
                    # Добавляем пометку в описание, если бюджет высокий
                    final_description = description
                    if price_limit >= PRIORITY_BUDGET:
                        final_description = "🔥 ВЫСОКИЙ БЮДЖЕТ! 🔥\n\n" + description

                    send_project(
                        category, 
                        SITE_NAME, 
                        price_limit, 
                        number_of_responses, 
                        final_description,
                        f"https://kwork.ru/projects/{id_}"
                    )
            
            # Ограничиваем размер файла (храним последние 2000 ID)
            if len(ignore_ids) > 2000:
                ignore_ids = ignore_ids[-1000:]
                with open("seen_ids.txt", "w") as f:
                    f.write("\n".join(ignore_ids) + "\n")

        except Exception as e:
            logging.error(f"Критическая ошибка в цикле парсинга: {e}")

        first_run = False
        await asyncio.sleep(10)  # Спим 10 секунд, чтобы не забанили IP

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
