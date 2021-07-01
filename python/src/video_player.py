"""A video player class."""
import random

from video_library import VideoLibrary
from video_playlist import Playlist
from random import randint


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlists = []
        self._currently_playing_video = None # tracks the currently playing video
        self._paused = False # tracks the pause state of the video player

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        # iterates over all the videos and uses the inbuilt printout function to print them to the terminal
        for video in videos:
            video.printout()
            if video.is_flagged:
                print(f" - FLAGGED (reason: {video.flag_reason})", end="")
            print()

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot play video: Video does not exist")
            return

        # cehcks that there is a video currently playing and stops it if true
        if self._currently_playing_video != None:
            self.stop_video()

        # checking that the video isn't flagged
        if video.is_flagged:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")
            return

        # checking if the video with video_id exists
        print(f"Playing video: {video.title}")

        # sets the currently playing video - will be None if the video with video_id does not exist
        self._currently_playing_video = video

    def stop_video(self):
        """Stops the current video."""
        self._paused = False
        # checking if there is a video already playing
        if self._currently_playing_video:
            print(f"Stopping video: {self._currently_playing_video.title}")
            self._currently_playing_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        # takes a random video from all the videos in the video library
        video = random.choice(self._video_library.get_all_videos())
        if video.is_flagged:
            print("No videos available")
            return
        self.play_video(video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self._paused:
            print(f"Video already paused: {self._currently_playing_video.title}")
        elif not self._currently_playing_video:
            print("Cannot pause video: No video is currently playing")
        else:
            print(f"Pausing video: {self._currently_playing_video.title}")
            self._paused = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self._paused:
            print(f"Continuing video: {self._currently_playing_video.title}")
            self._paused = False
        elif not self._currently_playing_video:
            print("Cannot continue video: No video is currently playing")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self._currently_playing_video:
            print(f"Currently playing: ", end="")
            self._currently_playing_video.printout()
            if self._paused:
                print(" - PAUSED", end="")
            print()
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name: str):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._find_playlist(playlist_name) != None:
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        new_playlist = Playlist(playlist_name)
        self._playlists.append(new_playlist)
        print(f"Successfully created new playlist: {new_playlist.name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self._find_playlist(playlist_name)

        if playlist == None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return

        video = self._video_library.get_video(video_id)

        if video == None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video.is_flagged:
            print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {video.flag_reason})")
            return

        for playlist_video in playlist.videos:
            if playlist_video.video_id == video.video_id:
                print(f"Cannot add video to {playlist.name}: Video already added")
                return
        playlist.add_video(video)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlists) == 0:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        self._playlists.reverse() # reverse the list to show the newest added playlists first
        for pl in self._playlists:
            print(pl.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._find_playlist(playlist_name)
        if playlist == None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Showing playlist: {playlist_name}")
        if len(playlist.videos) == 0:
            print("No videos here yet")
            return

        for video in playlist.videos:
            video.printout()
            if video.is_flagged:
                print(f" - FLAGGED (reason: {video.flag_reason})", end="")
            print()

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        in_library = False
        for video in self._video_library.get_all_videos():
            if video_id == video.video_id:
                in_library = True
        if in_library == False:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        playlist = self._find_playlist(playlist_name)
        # Check that the playlist exists
        if playlist == None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        # check if the video is contained within the playlist
        #   remove if found and return
        playlist = self._find_playlist(playlist_name)
        for i, video in enumerate(playlist.videos):
            if video.video_id == video_id:
                print(f"Removed video from {playlist_name}: {video.title}")
                playlist.videos.pop(i)
                return

        # if the video is not in the playlist
        print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._find_playlist(playlist_name)
        if playlist == None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        playlist.clear_videos()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # finding the playlist in the _playlists list and removing it
        for i, pl in enumerate(self._playlists):
            if pl.name.lower() == playlist_name.lower():
                self._playlists.pop(i)
                print(f"Deleted playlist: {playlist_name}")
                return

        # if the playlist_name is not in the playlist list
        print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def _find_playlist(self, playlist_name) -> Playlist:
        """
        searches through the playlists property to see if the playlist_name is in there

        Args:
            playlist_name: The playlist name.
        """
        for pl in self._playlists:
            if pl.name.lower() == playlist_name.lower():
                return pl

        # returns None if the playlist has not been created
        return None

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        # searching through videos for videos titles containing search_term and adding them to a list
        videos = []
        for video in self._video_library.get_all_videos():
            if search_term.lower() in video.title.lower():
                if video.is_flagged:
                    continue
                videos.append(video)

        # printing the search results
        if len(videos) == 0:
            # inform the user of no results and exit function
            print(f"No search results for {search_term}")
            return
        else:
            self._print_search_results(search_term, videos)

        # asking the user to pick a result
        choice = self._ask_for_choice(videos)
        if choice == -1:
            return

        # if everything is fine play the video chosen
        #   choice-1 as indexes sart from 0 and choices from 1
        self.play_video(videos[choice-1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        # searching through the videos for matching tags and adding them to a list
        videos = []
        for video in self._video_library.get_all_videos():
            for tag in video.tags:
                if tag == video_tag:
                    if video.is_flagged:
                        continue
                    videos.append(video)

        # printing the search results
        if len(videos) == 0:
            # inform the user of no results and exit function
            print(f"No search results for {video_tag}")
            return
        else:
            self._print_search_results(video_tag, videos)

        # asking the user to pick a result
        choice = self._ask_for_choice(videos)
        if choice == -1:
            return

        # if everything is fine play the video chosen
        #   choice-1 as indexes sart from 0 and choices from 1
        self.play_video(videos[choice-1].video_id)

    def _print_search_results(self, search_term, videos):
        """
        takes a list of videos and prints them for the user to choose from

        args:
            videos: a list of Video objects
        """
        # if no videos are found inform user and return
        print(f"Here are the results for {search_term}:")
        for i, video in enumerate(videos):
            print(f"{i+1}) ", end='')
            video.printout()
            print()

    def _ask_for_choice(self, videos):
        """
        allows a user to pick a result from a search

        :return: choice (int) if all validity tests passed, else -1
        """
        # asking the user for what result number they want to play
        print("Would you like to play any of the above? If yes, specify the number of the video. \n"
              "If your answer is not a valid number, we will assume it's a no. ", end="")
        choice = input()

        # makes sure that the choice is a valid integer
        try:
            choice = int(choice)
        except ValueError:
            return -1

        # if the number does not match a search result then return
        if choice < 1 or choice > len(videos):
            return -1

        # returns choice if all validity tests pass
        return choice

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print('Cannot flag video: Video does not exist')
            return

        if video.is_flagged == True:
            print('Cannot flag video: Video is already flagged')
            return

        # stops current video if it has been flagged
        if video == self._currently_playing_video:
            self.stop_video()

        # informs the user the video has been flagged and adds the reason to the video object
        if flag_reason != "":
            video.flag(flag_reason)
            print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
        else:
            video.flag("")
            print(f"Successfully flagged video: {video.title} (reason: Not supplied)")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)

        # checking that the video exists
        if not video:
            print("Cannot remove flag from video: Video does not exist")
            return

        if video.is_flagged:
            video.allow()
            print(f"Successfully removed flag from video: {video.title}")
        else:
            print("Cannot remove flag from video: Video is not flagged")
