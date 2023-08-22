import os
import json

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

    def to_json(self, data):
        """
        Сохраняет значение атрибутов экземпляра класса в файл json
        """
        dict_channel = {'channel_id': self.channel_id, 'title': self.title, 'description': self.description,
                        'url': self.url, 'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                        'view_count': self.view_count}
        with open(data, 'a') as file:
            if os.stat(data).st_size == 0:
                json.dump([dict_channel], file)
            else:
                with open(data) as json_file:
                    data_json = json.load(json_file)
                data_json.append(dict_channel)
                with open(data, 'w') as json_file:
                    json.dump([data_json], json_file)
