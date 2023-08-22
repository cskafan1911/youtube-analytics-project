import os
import json
import isodate

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # Переменная окружения
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    # @staticmethod
    # def get_info():
    #     """
    #     Возвращает информацию о канале
    #     """
    #     info_channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics')


