import requests
import re
import asyncio
import json
import logging
import random
from parsers.send_project import send_project

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SITE_NAME = "kwork"
SITE_URL = "https://kwork.ru/projects"

# Наши ключевые слова для фильтрации (в нижнем регистре)
KEYWORDS = [
    "python", "телеграм", "бот", "парсер", "автоматизация", 
    "авито", "excel", "таблицы", "скрипт", "ai", "ии", 
    "чат-бот", "парсинг", "выгрузка", "автоответчик",
    "selenium", "playwright", "scraping", "wildberries", 
    "ozon", "яндекс маркет", "сбермегамаркет", "cloudfare",
    "антидетект", "скрейпинг"
]

# Ключевые слова для приоритетных ниш (наш опыт)
PRIORITY_KEYWORDS = ["arlight", "blesslight", "светотехника", "светильники", "освещение", "люстры"]

MIN_BUDGET = 0  # Теперь шлем вообще всё, как ты и просил
PRIORITY_BUDGET = 3000  # Пометка "Высокий бюджет" остается для ориентира

def contains_keywords(text, keywords_list=KEYWORDS):
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords_list)


with open("cats.json", "r", encoding="utf-8") as f:
    cats = json.load(f)

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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(SITE_URL, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logging.error(f"Ошибка доступа к сайту: {response.status_code}")
                await asyncio.sleep(random.randint(60, 120))
                continue

            match = re.search(r"window\.stateData=(.*?)};", response.text)
            if not match:
                logging.error("Не удалось найти stateData на странице")
                await asyncio.sleep(random.randint(60, 120))
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

                if id_ in ignore_ids:
                    continue
                
                ignore_ids.append(id_)
                # Сразу записываем в файл, чтобы не потерять при падении
                with open("seen_ids.txt", "a") as f:
                    f.write(f"{id_}\n")
                
                # ФИЛЬТРАЦИЯ
                is_relevant = contains_keywords(name) or contains_keywords(description)
                is_priority_niche = contains_keywords(name, PRIORITY_KEYWORDS) or contains_keywords(description, PRIORITY_KEYWORDS)
                is_good_budget = price_limit >= MIN_BUDGET
                
                if (is_relevant and is_good_budget) or price_limit >= PRIORITY_BUDGET or is_priority_niche:
                    logging.info(f"Найдено совпадение! {name} ({price_limit} руб.)")
                    
                    final_description = description
                    if is_priority_niche:
                        final_description = "🌟 ИДЕАЛЬНОЕ СОВПАДЕНИЕ (НИША) 🌟\n\n" + description
                    elif price_limit >= PRIORITY_BUDGET:
                        final_description = "🔥 ВЫСОКИЙ БЮДЖЕТ! 🔥\n\n" + description

                    send_project(
                        category, 
                        SITE_NAME, 
                        price_limit, 
                        number_of_responses, 
                        final_description,
                        f"https://kwork.ru/projects/{id_}",
                        id_,
                        name
                    )


            
            # Ограничиваем размер файла (храним последние 2000 ID)
            if len(ignore_ids) > 2000:
                ignore_ids = ignore_ids[-1000:]
                with open("seen_ids.txt", "w") as f:
                    f.write("\n".join(ignore_ids) + "\n")

        except Exception as e:
            logging.error(f"Критическая ошибка в цикле парсинга: {e}")

        first_run = False
        # Увеличиваем интервал до безопасного (1.5 - 3 минуты), чтобы имитировать человека и избежать капчи
        await asyncio.sleep(random.randint(90, 180))

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
