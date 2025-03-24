import os
import re
from pytube import YouTube
from config import DOWNLOAD_DIR, TEMP_DIR

def is_valid_youtube_url(url):
    """Проверка, является ли ссылка допустимой ссылкой YouTube"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return bool(re.match(youtube_regex, url))

def get_video_info(url):
    """Получение информации о видео"""
    try:
        yt = YouTube(url)
        
        # Собираем доступные разрешения
        resolutions = []
        
        # Получаем доступные разрешения для видео
        video_streams = yt.streams.filter(progressive=True).order_by('resolution')
        for stream in video_streams:
            if stream.resolution:
                resolution = stream.resolution.replace('p', '')
                if resolution in ['480', '720', '1080'] and resolution not in resolutions:
                    resolutions.append(resolution)
        
        # Проверяем, есть ли аудиопоток
        audio_stream = yt.streams.filter(only_audio=True).first()
        has_audio = audio_stream is not None
        
        return {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'thumbnail': yt.thumbnail_url,
            'resolutions': resolutions,
            'has_audio': has_audio
        }
    except Exception as e:
        print(f"Ошибка при получении информации о видео: {e}")
        return None

def download_video(url, resolution='720'):
    """Загрузка видео с YouTube"""
    try:
        yt = YouTube(url)
        
        # Создаем безопасное имя файла
        safe_title = "".join([c for c in yt.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        file_path = os.path.join(DOWNLOAD_DIR, f"{safe_title}_{resolution}p.mp4")
        
        # Загружаем видео нужного разрешения
        if resolution == 'audio':
            # Загружаем только аудио в формате mp3
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=DOWNLOAD_DIR, filename=f"{safe_title}.mp3")
            file_path = out_file
        else:
            # Загружаем видео с выбранным разрешением
            stream = yt.streams.filter(res=f"{resolution}p", progressive=True).first()
            
            # Если нет прогрессивного потока с нужным разрешением, пробуем найти наиболее близкое
            if not stream:
                stream = yt.streams.filter(progressive=True).order_by('resolution').last()
            
            out_file = stream.download(output_path=DOWNLOAD_DIR, filename=f"{safe_title}_{resolution}p.mp4")
            file_path = out_file
        
        # Получаем размер файла
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # в МБ
        
        return {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': file_size,
            'format': 'mp3' if resolution == 'audio' else 'mp4'
        }
    
    except Exception as e:
        print(f"Ошибка при загрузке видео: {e}")
        return None 