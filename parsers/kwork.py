import requests
import re
import asyncio
import json
from parsers.send_project import send_project

SITE_NAME = "kwork"
SITE_URL = "https://kwork.ru/projects"
CATEGORIES = {
    1: ""
}

with open("cats.json", "r", encoding="utf 8") as f:
    cats = json.load(f)


async def main():
    ignore_ids = []
    first_run = True

    while True:
        try:
            request = requests.get(SITE_URL, timeout=15)
            data = re.search(r"window\.stateData=(.*?)};", request.text).group(1) + "}"
            data = json.loads(data)
            wants_list = data["wantsListData"]["wants"]
            for want in wants_list:
                id_ = want["id"]
                # print(id_)
                name = want["name"]
                description = want["description"]
                number_of_responses = want["kwork_count"]
                category_id = want["category_id"]
                category = cats[category_id]
                price_limit = round(float(want["priceLimit"]))

                if first_run:
                    ignore_ids.append(id_)
                if id_ in ignore_ids:
                    continue

                ignore_ids.append(id_)
                await send_project(category, SITE_NAME, price_limit, number_of_responses, description,
                                   f"https://kwork.ru/projects/{id_}")
        except:
            print("ex!")

        first_run = False
        await asyncio.sleep(5)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
