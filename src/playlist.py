import os
import datetime
import isodate

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
        self.playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                          part='contentDetails, snippet',
                                                          maxResults=50).execute()

        self.title = self.playlist['items'][0]['snippet']['title'].split(".")[0]
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        total_duration = datetime.timedelta()
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            hour, minute, second = str(duration).split(":")
            total_duration += datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))

        return total_duration
