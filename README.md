# kwork-tracker

Telegram-бот для отслеживания заказов с фриланс-бирж (в текущей версии используется парсер `kwork`) с фильтрацией по категориям и отправкой уведомлений пользователям. None-vibecode, проект написан в 2023 году. Запущен на https://t.me/OrdersTrackerBot

## Возможности

- Запуск Telegram-бота на `aiogram`.
- Парсинг новых заказов в фоне.
- Хранение пользовательских настроек в `SQLite` (`users.db`).
- Настройки текста, категорий и бирж через `settings.json`.

## Требования

- Python `3.11` (рекомендуется; `3.13` не подходит для зависимостей проекта).
- Файл `settings.json` в корне проекта.

## Настройка

1. Скопируй шаблон:

```bash
cp settings.example.json settings.json
```

2. Заполни минимум:
- `token` — токен Telegram-бота.
- `channels` — список каналов для проверки подписки (если используешь этот режим).
- `texts`/`categories`/`exchanges` — при необходимости под свои задачи.

## Локальный запуск (Linux/macOS)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
python main.py
```

## Структура проекта

- `main.py` — точка входа, запуск бота и фонового парсера.
- `parsers/` — парсеры бирж.
- `commands/`, `buttons/`, `utils/callback` — обработчики команд и callback-кнопок.
- `base/` — работа с БД.
- `settings.example.json` — шаблон конфигурации.