import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Токен бота Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Учетные данные MEGA
MEGA_EMAIL = os.getenv('MEGA_EMAIL')
MEGA_PASSWORD = os.getenv('MEGA_PASSWORD')

# MongoDB подключение
MONGODB_URI = os.getenv('MONGODB_URI')

# ID администратора бота
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0))

# Временные каталоги
DOWNLOAD_DIR = "downloads"
TEMP_DIR = "temp"

# Время жизни ссылки и файла на MEGA (в секундах)
LINK_EXPIRATION_TIME = 3600  # 1 час 