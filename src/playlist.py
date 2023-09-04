import os

from googleapiclient.discovery import build


class PlayList:
    """
    Класс для Плейлиста
    """
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        """
        Инициализация плейлиста по id
        """

        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                 maxResults=50).execute()

