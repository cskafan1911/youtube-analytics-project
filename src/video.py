import os

from googleapiclient.discovery import build


class Video:
    """
    Класс для видео
    """
    # Переменная окружения
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id) -> None:
        """
        Экземпляр инициализирует id video. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id

        try:
            self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
            self.title = self.video['items'][0]['snippet']['title']
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']

        except IndexError:
            self.video = None
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """
        Возвращает название видео
        """
        return f"{self.title}"


class PLVideo(Video):
    """
    Класс для плейлиста
    """

    def __init__(self, video_id, play_list_id):
        """
        Экземпляр инициализирует id видео, id плейлиста
        """
        super().__init__(video_id)
        self.play_list_id = play_list_id
