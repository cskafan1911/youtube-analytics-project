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
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        self.title = self.playlist['items'][0]['snippet']['title'].split(".")[0]
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    @property
    def total_duration(self):
        """
        Объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        total_duration = datetime.timedelta()
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            hour, minute, second = str(duration).split(":")
            total_duration += datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        likes_list = {}

        for video_id in self.video_ids:
            video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()
            likes_list[('https://youtu.be/' + video['items'][0]['id'])] = (
                int(video['items'][0]['statistics']['likeCount']))

        values_ = list(likes_list.values())
        keys_ = list(likes_list.keys())
        return keys_[values_.index(max(values_))]
