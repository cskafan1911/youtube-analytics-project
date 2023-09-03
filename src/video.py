import os

from googleapiclient.discovery import build


class Video:
    """
    Класс для видео
    """
    # Переменная окружения
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

