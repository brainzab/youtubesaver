import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, BigInteger, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URL

# Создаем соединение с базой данных
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Определяем модели данных
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_active = Column(DateTime, default=datetime.now)
    total_downloads = Column(Integer, default=0)
    registered_at = Column(DateTime, default=datetime.now)
    
    # Отношения
    downloads = relationship("Download", back_populates="user")

class Download(Base):
    __tablename__ = 'downloads'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    youtube_url = Column(String(255))
    quality = Column(String(50))
    file_size = Column(Float)
    file_format = Column(String(10))
    timestamp = Column(DateTime, default=datetime.now)
    
    # Отношения
    user = relationship("User", back_populates="downloads")

class MegaFile(Base):
    __tablename__ = 'mega_files'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255), unique=True)
    path = Column(String(255))
    link = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.now)
    expiration_time = Column(DateTime)

# Создаем таблицы в базе данных
def init_db():
    Base.metadata.create_all(engine)

# Инициализация базы данных при импорте
init_db()

def register_user(user_id, username, first_name):
    """Регистрация нового пользователя или обновление информации о существующем"""
    session = Session()
    
    try:
        existing_user = session.query(User).filter_by(user_id=user_id).first()
        
        if existing_user:
            existing_user.username = username
            existing_user.first_name = first_name
            existing_user.last_active = datetime.now()
            session.commit()
            return False
        else:
            new_user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_active=datetime.now(),
                total_downloads=0,
                registered_at=datetime.now()
            )
            session.add(new_user)
            session.commit()
            return True
    finally:
        session.close()

def update_user_activity(user_id):
    """Обновление времени последней активности пользователя"""
    session = Session()
    
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.last_active = datetime.now()
            session.commit()
    finally:
        session.close()

def increment_download_count(user_id):
    """Увеличение счетчика загрузок для пользователя"""
    session = Session()
    
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.total_downloads += 1
            session.commit()
    finally:
        session.close()

def log_download(user_id, youtube_url, quality, file_size, file_format):
    """Логирование загрузки в базе данных"""
    session = Session()
    
    try:
        download = Download(
            user_id=user_id,
            youtube_url=youtube_url,
            quality=quality,
            file_size=file_size,
            file_format=file_format,
            timestamp=datetime.now()
        )
        session.add(download)
        session.commit()
    finally:
        session.close()

def register_mega_file(file_id, path, link, expiration_time):
    """Регистрация файла, загруженного на MEGA"""
    session = Session()
    
    try:
        mega_file = MegaFile(
            file_id=file_id,
            path=path,
            link=link,
            uploaded_at=datetime.now(),
            expiration_time=expiration_time
        )
        session.add(mega_file)
        session.commit()
    finally:
        session.close()

def get_expired_mega_files():
    """Получение списка истекших файлов на MEGA"""
    session = Session()
    
    try:
        current_time = datetime.now()
        expired_files = session.query(MegaFile).filter(MegaFile.expiration_time < current_time).all()
        return expired_files
    finally:
        session.close()

def delete_mega_file_record(file_id):
    """Удаление записи о файле MEGA из базы данных"""
    session = Session()
    
    try:
        session.query(MegaFile).filter_by(file_id=file_id).delete()
        session.commit()
    finally:
        session.close()

def get_stats():
    """Получение статистики для администратора"""
    session = Session()
    
    try:
        # Общее количество пользователей
        total_users = session.query(func.count(User.id)).scalar()
        
        # Общее количество загрузок
        total_downloads = session.query(func.count(Download.id)).scalar()
        
        # Сегодняшняя дата с временем 00:00:00
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Загрузки сегодня
        downloads_today = session.query(func.count(Download.id)).filter(Download.timestamp >= today).scalar()
        
        # Активные пользователи сегодня
        active_users_today = session.query(func.count(User.id)).filter(User.last_active >= today).scalar()
        
        # Топ пользователей по загрузкам
        top_users = session.query(User).order_by(User.total_downloads.desc()).limit(5).all()
        
        # Преобразуем объекты User в словари
        top_users_list = []
        for user in top_users:
            top_users_list.append({
                'user_id': user.user_id,
                'username': user.username,
                'first_name': user.first_name,
                'total_downloads': user.total_downloads
            })
        
        return {
            'total_users': total_users,
            'total_downloads': total_downloads,
            'downloads_today': downloads_today,
            'active_users_today': active_users_today,
            'top_users': top_users_list
        }
    finally:
        session.close() 