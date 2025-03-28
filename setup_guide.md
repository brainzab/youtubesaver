# Руководство по установке и настройке YouTube Downloader Bot

## Содержание
1. [Подготовка](#подготовка)
2. [Создание бота в Telegram](#создание-бота-в-telegram)
3. [Регистрация аккаунта MEGA](#регистрация-аккаунта-mega)
4. [Настройка PostgreSQL](#настройка-postgresql)
5. [Локальная установка](#локальная-установка)
6. [Деплой на Railway](#деплой-на-railway)
7. [Устранение неполадок](#устранение-неполадок)

## Подготовка

Перед началом работы необходимо убедиться, что у вас есть:
- Аккаунт Telegram
- Аккаунт на MEGA (или готовность его создать)
- Аккаунт GitHub (для деплоя на Railway)
- Аккаунт Railway (если планируете размещать бота на этой платформе)
- Python 3.8+ (для локального запуска)
- PostgreSQL (для хранения данных)

## Создание бота в Telegram

1. Откройте Telegram и найдите бота [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям BotFather:
   - Введите имя для бота (например, "YouTube Downloader Bot")
   - Введите уникальное имя пользователя для бота (должно заканчиваться на "bot")
4. После создания бота BotFather отправит вам сообщение с токеном бота. Сохраните этот токен, он потребуется для настройки.
5. Для получения своего ID в Telegram, найдите бота [@userinfobot](https://t.me/userinfobot) и отправьте ему любое сообщение. Он ответит вам информацией о вашем аккаунте, включая ID.

## Регистрация аккаунта MEGA

1. Перейдите на сайт [MEGA](https://mega.nz/register) и зарегистрируйте новый аккаунт
2. Рекомендуется создать отдельный аккаунт для бота
3. После регистрации запомните email и пароль - они потребуются для настройки

## Настройка PostgreSQL

Для сбора статистики и хранения данных необходимо настроить базу данных PostgreSQL.

### Локальная установка PostgreSQL

1. Скачайте и установите PostgreSQL с [официального сайта](https://www.postgresql.org/download/)
2. Во время установки задайте пароль для пользователя postgres
3. После установки создайте новую базу данных:
   - Откройте pgAdmin или командную строку psql
   - Выполните SQL-запрос: `CREATE DATABASE youtube_downloader;`
4. Строка подключения к базе данных будет иметь следующий формат:
   `postgresql://username:password@localhost:5432/youtube_downloader`

### Использование PostgreSQL в Railway

Railway предоставляет PostgreSQL как сервис:

1. В панели управления Railway выберите "New Project"
2. Выберите "Provision PostgreSQL"
3. После создания базы данных, перейдите на вкладку "Variables"
4. Скопируйте значение переменной `DATABASE_URL` - это и есть ваша строка подключения

## Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/username/youtube-downloader-bot.git
cd youtube-downloader-bot
```

2. Создайте виртуальное окружение Python:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. Создайте файл `.env` в корневой директории проекта и добавьте следующие строки:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MEGA_EMAIL=your_mega_email
MEGA_PASSWORD=your_mega_password
DATABASE_URL=postgresql://username:password@localhost:5432/youtube_downloader
ADMIN_USER_ID=your_telegram_user_id
```

6. Запустите бота:
```bash
python bot.py
```

7. Теперь бот должен быть онлайн и готов к использованию. Проверьте его работу, отправив команду `/start` боту в Telegram.

## Деплой на Railway

### Шаг 1: Подготовка репозитория GitHub

1. Создайте новый репозиторий на GitHub
2. Загрузите все файлы проекта в репозиторий:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/your-repo-name.git
git push -u origin main
```

### Шаг 2: Настройка проекта на Railway

1. Зарегистрируйтесь на [Railway](https://railway.app/)
2. После входа в аккаунт нажмите кнопку "New Project"
3. Сначала создайте сервис PostgreSQL: выберите "Provision PostgreSQL"
4. Затем создайте сервис из GitHub: выберите "Deploy from GitHub repo"
5. Предоставьте Railway доступ к вашему GitHub аккаунту и выберите репозиторий с ботом
6. Railway автоматически определит, что это Python-проект и настроит базовое окружение

### Шаг 3: Настройка переменных окружения на Railway

1. В панели управления проектом перейдите во вкладку "Variables"
2. Добавьте следующие переменные окружения:
   - `TELEGRAM_BOT_TOKEN` - токен вашего бота
   - `MEGA_EMAIL` - email аккаунта MEGA
   - `MEGA_PASSWORD` - пароль аккаунта MEGA
   - `ADMIN_USER_ID` - ваш Telegram ID
3. Переменная `DATABASE_URL` должна быть автоматически добавлена при создании PostgreSQL сервиса

### Шаг 4: Завершение деплоя

1. После добавления переменных окружения Railway автоматически перезапустит ваш сервис
2. Перейдите во вкладку "Deployments", чтобы убедиться, что ваш бот успешно запущен
3. Если вы видите "Deployment successful", значит бот работает
4. Проверьте работу бота, отправив ему команду `/start` в Telegram

## Устранение неполадок

### Бот не отвечает
1. Проверьте, правильно ли указан токен бота в переменных окружения
2. Убедитесь, что приложение успешно запущено (локально или на Railway)
3. Проверьте логи на наличие ошибок

### Проблемы с загрузкой видео
1. Убедитесь, что ссылка на видео действительна и видео не удалено с YouTube
2. Проверьте права доступа к директориям `downloads` и `temp`
3. Убедитесь, что у вас достаточно свободного места на сервере

### Проблемы с MEGA
1. Проверьте правильность учетных данных MEGA
2. Убедитесь, что на аккаунте MEGA достаточно свободного места
3. Если используете бесплатный аккаунт MEGA, помните о лимитах на трафик

### Проблемы с PostgreSQL
1. Проверьте правильность строки подключения DATABASE_URL
2. Если используете локальную БД, убедитесь, что PostgreSQL запущен и доступен
3. Проверьте права доступа пользователя к базе данных
4. Если возникает ошибка "relation does not exist", это значит, что таблицы еще не созданы. При первом запуске приложения они должны создаться автоматически

Если у вас остались вопросы или проблемы при настройке бота, создайте issue в репозитории проекта на GitHub. 