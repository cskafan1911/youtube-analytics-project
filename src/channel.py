import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # Переменная окружения
    API_KEY = os.getenv('YOUTUBE_API_KEY')

    # Данные для работы с API youtube
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        print(channel)
