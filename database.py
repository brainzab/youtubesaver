import pymongo
from datetime import datetime
from config import MONGODB_URI

# Подключение к MongoDB
client = pymongo.MongoClient(MONGODB_URI)
db = client.youtube_downloader

# Коллекции
users = db.users
downloads = db.downloads
mega_files = db.mega_files

def register_user(user_id, username, first_name):
    """Регистрация нового пользователя или обновление информации о существующем"""
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_active": datetime.now(),
        "total_downloads": 0,
        "registered_at": datetime.now()
    }
    
    existing_user = users.find_one({"user_id": user_id})
    if existing_user:
        users.update_one(
            {"user_id": user_id},
            {"$set": {
                "username": username,
                "first_name": first_name,
                "last_active": datetime.now()
            }}
        )
        return False
    else:
        users.insert_one(user_data)
        return True

def update_user_activity(user_id):
    """Обновление времени последней активности пользователя"""
    users.update_one(
        {"user_id": user_id},
        {"$set": {"last_active": datetime.now()}}
    )

def increment_download_count(user_id):
    """Увеличение счетчика загрузок для пользователя"""
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"total_downloads": 1}}
    )

def log_download(user_id, youtube_url, quality, file_size, file_format):
    """Логирование загрузки в базе данных"""
    download_data = {
        "user_id": user_id,
        "youtube_url": youtube_url,
        "quality": quality,
        "file_size": file_size,
        "file_format": file_format,
        "timestamp": datetime.now()
    }
    downloads.insert_one(download_data)

def register_mega_file(file_id, path, link, expiration_time):
    """Регистрация файла, загруженного на MEGA"""
    file_data = {
        "file_id": file_id,
        "path": path,
        "link": link,
        "uploaded_at": datetime.now(),
        "expiration_time": expiration_time
    }
    mega_files.insert_one(file_data)

def get_expired_mega_files():
    """Получение списка истекших файлов на MEGA"""
    current_time = datetime.now()
    return list(mega_files.find({
        "expiration_time": {"$lt": current_time}
    }))

def delete_mega_file_record(file_id):
    """Удаление записи о файле MEGA из базы данных"""
    mega_files.delete_one({"file_id": file_id})

def get_stats():
    """Получение статистики для администратора"""
    total_users = users.count_documents({})
    total_downloads = downloads.count_documents({})
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    downloads_today = downloads.count_documents({"timestamp": {"$gte": today}})
    
    active_users_today = users.count_documents({"last_active": {"$gte": today}})
    
    top_users = list(users.find().sort("total_downloads", -1).limit(5))
    
    return {
        "total_users": total_users,
        "total_downloads": total_downloads,
        "downloads_today": downloads_today,
        "active_users_today": active_users_today,
        "top_users": top_users
    } 