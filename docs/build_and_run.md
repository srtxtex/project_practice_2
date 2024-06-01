# Как собрать и запустить проект

## Шаг 1: Клонирование репозитория

Клонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/srtxtex/project_practice_2.git cd project_practice_2
```


## Шаг 2: Установка зависимостей

Установите все необходимые зависимости, выполнив следующую команду:

```bash
pip install -r requirements.txt
```


## Шаг 3: Настройка окружения

Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:

```plaintext
TOKEN=your_telegram_bot_token
LL_MODEL=your_large_language_model_identifier
```


## Шаг 4: Запуск бота

Запустите чат-бота, используя следующую команду:

```bash
python src/tg_bot.py
```

Теперь бот готов к работе!
