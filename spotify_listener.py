'''
Module that holds all the spotify request APIs
'''
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class TrackInfo():
    '''
    Storage class for track data
    '''
    def __init__(self) -> None:
        self.track_name = ""
        self.artists = []
        self.is_playing = False
        self.current_pos_ms = 0
        self.track_dur_ms = 0

class SpotifyConnection():
    '''
    Class that queries and stores the Spotify user's current track data
    '''
    def __init__(self) -> None:
        self.scope = "user-read-currently-playing"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.current_track = TrackInfo()

    def update(self) -> None:
        '''
        Retrieves the current track data and stores it
        '''
        results = self.spotify.current_user_playing_track()
        if results is None:
            print("No current playing track")
            return
        new_track = TrackInfo()
        new_track.track_name = results["item"]["name"]
        new_track.current_pos_ms = results["progress_ms"]
        new_track.track_dur_ms = results["item"]["duration_ms"]
        new_track.is_playing= results["is_playing"]
        # new_track.artists.clear()
        for artist in results["item"]["artists"]:
            new_track.artists.append(artist["name"])
        self.current_track = new_track

    def get_current_track(self) -> TrackInfo:
        '''
        Get current playing track
        '''
        return self.current_track
