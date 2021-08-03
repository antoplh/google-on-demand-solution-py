"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist

from random import randrange

# please note I didn't notice there was already a solution file published, and proceeded to code my own
# I would've liked for the solutions to be uploaded after the on-demand experience
# I enjoyed my time solving this, thus I'm choosing to upload this work rather than the EY project option
# I also enjoyed watching the seminares, and would definitely join again in the future, if my schedule (and sleep schedule) allows it
# Sincerely, 
# Someone from the EST-ish timezone

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._my_playlists = []
        self._current_video = None
        self._video_stat = None


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = [video for video in self._video_library.get_all_videos()]
        videos = sorted(videos, key = lambda x: x.title)

        print("Here's a list of all available videos:")
        for video in videos:
            print(video.format_video())

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        videos = dict([[video.video_id, video] for video in self._video_library.get_all_videos()])

        if video_id in videos:
            if videos[video_id].flagged == False:
                if self._current_video != None and self._video_stat != 'STP':
                    self.stop_video()
                self._current_video = videos[video_id]
                self._video_stat = 'PLY'
                print (f"Playing video: {self._current_video.title}")
            else:
                print(f"Cannot play video: Video is currently flagged (reason: {videos[video_id].flagged_reason})")
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        if self._current_video == None or self._video_stat == 'STP' or self._current_video.flagged == True:
            print("Cannot stop video: No video is currently playing")

        else:
            self._stopped_video = self._current_video
            self._video_stat = 'STP'
            print(f"Stopping video: {self._current_video.title}")

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = [video for video in self._video_library.get_all_videos()]
        available = []
        for video in videos:
            if video.flagged == False:
                available.append(video)

        if len(available) > 0:
            random_video = available[randrange(len(available))]
            self.play_video(random_video.video_id)
        else:
            print("No videos available")


    def pause_video(self):
        """Pauses the current video."""
        if self._video_stat == 'PS':
            print(f"Video already paused: {self._current_video.title}")
        elif self._current_video == None or self._current_video.flagged == True:
            print("Cannot pause video: No video is currently playing")
        else:
            self._video_stat = 'PS'
            print(f"Pausing video: {self._current_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if self._current_video == None:
            print("Cannot continue video: No video is currently playing")
        elif self._video_stat == 'PLY':
            print("Cannot continue video: Video is not paused")
        else:
            self._video_stat = 'PLY'
            print(f"Continuing video: {self._current_video.title}")

    def show_playing(self):
        """Displays video currently playing."""
        video = self._current_video
        if video == None or self._current_video.flagged == True:
            print('No video is currently playing')
        elif self._video_stat == 'PS':
            print(f"Currently playing: {video.format_video()} - PAUSED")
        else:
            print(f"Currently playing: {video.format_video()}")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        names = [playlist.name for playlist in self._my_playlists]

        if playlist_name.upper() in list(map(str.upper,names)):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:   
            new_playlist = Playlist(playlist_name)
            self._my_playlists.append(new_playlist)
            print(f"Successfully created new playlist: {new_playlist.name}")        
        

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        #video_id = video_id.replace('<','').replace('>','')
        videos = dict([[video.video_id, video] for video in self._video_library.get_all_videos()])
        playlists = dict([[playlist.name.upper(), playlist] for playlist in self._my_playlists])
    
        if playlist_name.upper() in playlists:
            if video_id in videos:
                current_playlist = playlists[playlist_name.upper()]
                pl_videos = [video.video_id for video in current_playlist.videos]
                if videos[video_id].flagged == False:
                    if video_id in pl_videos:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    elif video_id in videos:
                        current_playlist.add_video(videos[video_id])
                        print(f"Added video to {playlist_name}: {videos[video_id].title}")
                else:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {videos[video_id].flagged_reason})")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")        



    def show_all_playlists(self):
        """Display all playlists."""
        if self._my_playlists != []:
            playlists = [playlist.name for playlist in self._my_playlists]
            sorted_playlists = sorted(playlists)
            print("Showing all playlists:")
            for playlist in sorted_playlists:
                print(playlist)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlists = dict([[playlist.name.upper(), playlist] for playlist in self._my_playlists])

        if playlist_name.upper() in playlists:
            print(f"Showing playlist: {playlist_name}")
            if playlists[playlist_name.upper()].videos != []:
                videos = playlists[playlist_name.upper()].videos
                for video in videos:
                    print(f"{video.format_video()}")
            else:
                print("No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlists = dict([[playlist.name.upper(), playlist] for playlist in self._my_playlists])
        videos = dict([[video.video_id, video] for video in self._video_library.get_all_videos()])

        if playlist_name.upper() in playlists:
            if video_id in videos:
                pl_videos = dict([[video.video_id, video] for video in playlists[playlist_name.upper()].videos])
                if video_id in pl_videos:
                    index = self._my_playlists.index(playlists[playlist_name.upper()])
                    self._my_playlists[index].remove_video(pl_videos[video_id])
                    print(f"Removed video from {playlist_name}: {pl_videos[video_id].title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlists = dict([[playlist.name.upper(), playlist] for playlist in self._my_playlists])
        
        if playlist_name.upper() in playlists:
            index = self._my_playlists.index(playlists[playlist_name.upper()])
            self._my_playlists[index].clear_playlist()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlists = dict([[playlist.name.upper(), playlist] for playlist in self._my_playlists])
        
        if playlist_name.upper() in playlists:
            index = self._my_playlists.index(playlists[playlist_name.upper()])
            self._my_playlists.pop(index)
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = dict([[video.title, video] for video in self._video_library.get_all_videos()])
        results = []
        for title in videos:
            if search_term.upper() in title.upper() and videos[title].flagged == False:
                results.append(videos[title])
        
        if results != []:
            print(f"Here are the results for {search_term}:")
            for index in range(len(results)):
                print(f"{index + 1}) {results[index].format_video()}")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            answer = input()
            try:
                answer_video = results[int(answer) - 1].video_id
                self.play_video(answer_video)
            except:
                pass
        else:
            print(f"No search results for {search_term}")
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        video_tag = video_tag.replace('#','')
        videos = dict([[video.title, video] for video in self._video_library.get_all_videos()])
        results = []
        for title in videos:
            if video_tag.upper() in title.upper() and videos[title].flagged == False:
                results.append(videos[title])
        
        if results != []:
            print(f"Here are the results for #{video_tag}:")
            for index in range(len(results)):
                print(f"{index + 1}) {results[index].format_video()}")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            answer = input()
            try:
                answer_video = results[int(answer) - 1].video_id
                self.play_video(answer_video)
            except:
                pass
        else:
            print(f"No search results for #{video_tag}")


    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        videos = dict([[video.video_id, video] for video in self._video_library.get_all_videos()])
        
        if video_id in videos:
            video = videos[video_id]
            if video.flagged == False:
                if video == self._current_video:
                    self.stop_video()
                video.flag(flag_reason)
                print (f"Successfully flagged video: {video.title} (reason: {video.flagged_reason})")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        videos = dict([[video.video_id, video] for video in self._video_library.get_all_videos()])
        
        if video_id in videos:
            video = videos[video_id]
            if video.flagged == True:
                video.allow()
                print (f"Successfully removed flag from video: {video.title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")        
