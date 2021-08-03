"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name: str):
        self._name = name
        self._videos = []
    
    @property
    def name(self):
        """Returns a playlist name"""
        return self._name
    @property
    def videos(self):
        """Returns a playlist's videos"""
        return self._videos
    
    def add_video(self, video):
        """Adds a video object to the playlist"""
        self._videos.append(video)
    
    def remove_video(self, video):
        self._videos.remove(video)

    def clear_playlist(self):
        self._videos.clear()