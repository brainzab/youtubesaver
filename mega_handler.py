import os
import uuid
from datetime import datetime, timedelta
import shutil
from mega import Mega
from config import MEGA_EMAIL, MEGA_PASSWORD, DOWNLOAD_DIR, TEMP_DIR, LINK_EXPIRATION_TIME
from database import register_mega_file, get_expired_mega_files, delete_mega_file_record

# Инициализация директорий, если они не существуют
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Создаем экземпляр MEGA
mega = Mega()

# Функция для входа в MEGA
def login_to_mega():
    try:
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        return m
    except Exception as e:
        print(f"Ошибка при входе в MEGA: {e}")
        return None

# Функция для загрузки файла на MEGA
def upload_to_mega(file_path, file_name):
    try:
        m = login_to_mega()
        if not m:
            return None
        
        # Создаем папку для временных файлов, если она не существует
        folder_name = "youtube_downloads_temp"
        folders = m.get_files()
        
        # Проверяем, существует ли папка
        folder_exists = False
        folder_id = None
        
        for item_id, item_data in folders.items():
            if item_data['a'] and item_data['t'] == 1 and item_data['a']['n'] == folder_name:
                folder_exists = True
                folder_id = item_id
                break
        
        # Если папка не существует, создаем ее
        if not folder_exists:
            folder_id = m.create_folder(folder_name)
        
        # Загружаем файл в папку
        file = m.upload(file_path, dest=folder_id)
        
        # Получаем ссылку на файл
        link = m.get_upload_link(file)
        
        # Вычисляем время истечения
        expiration_time = datetime.now() + timedelta(seconds=LINK_EXPIRATION_TIME)
        
        # Регистрируем файл в базе данных
        register_mega_file(file, file_path, link, expiration_time)
        
        return {
            "file_id": file,
            "link": link,
            "expiration_time": expiration_time
        }
    
    except Exception as e:
        print(f"Ошибка при загрузке на MEGA: {e}")
        return None

# Функция для удаления файлов с истекшим сроком действия
def cleanup_expired_files():
    try:
        m = login_to_mega()
        if not m:
            return
        
        # Получаем просроченные файлы из базы данных
        expired_files = get_expired_mega_files()
        
        for file in expired_files:
            try:
                # Удаляем файл из MEGA
                m.delete(file.file_id)
                
                # Удаляем запись из базы данных
                delete_mega_file_record(file.file_id)
                
                # Если есть локальный файл, удаляем его
                if os.path.exists(file.path):
                    os.remove(file.path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file.file_id}: {e}")
    
    except Exception as e:
        print(f"Ошибка при очистке файлов: {e}")

# Функция для очистки временных локальных файлов
def cleanup_local_files():
    try:
        # Очищаем директории загрузок и временных файлов
        for dir_path in [DOWNLOAD_DIR, TEMP_DIR]:
            if os.path.exists(dir_path):
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
    except Exception as e:
        print(f"Ошибка при очистке локальных файлов: {e}") 