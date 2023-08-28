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
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """

        return cls.youtube

    @property
    def channel_id(self):
        """Геттер для channel_id"""

        return self.__channel_id

    def to_json(self, data):
        """
        Сохраняет значение атрибутов экземпляра класса в файл json
        """
        dict_channel = {'channel_id': self.__channel_id, 'title': self.title, 'description': self.description,
                        'url': self.url, 'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                        'view_count': self.view_count}
        with open(data, 'w') as file:
            if os.stat(data).st_size == 0:
                json.dump([dict_channel], file, indent=2, ensure_ascii=True)
            else:
                with open(data) as json_file:
                    data_json = json.load(json_file)
                data_json.append(dict_channel)
                with open(data, 'w') as json_file:
                    json.dump([data_json], json_file, indent=2, ensure_ascii=True)
        #
        # if os.path.exists(data): # проверили существует ли файл, если да:
        #     with open(data, 'r') as file:
        #         content = json.load(file) # считали список словарей в content
        # else:
        #     content = [] # создали пустой список в ту же content
        #     content.append(dict_channel) # добавили новый словарь в список (полученный или созданный, не важно)
        #     with open(data, 'w') as file:
        #         json.dump(content, file, ensure_ascii=False, indent=2) # дампим данные в файл
