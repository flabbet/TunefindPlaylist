from gmusicapi import Mobileclient
from gmusicapi.exceptions import NotLoggedIn


class PlaylistManager:
    client = Mobileclient()

    def __init__(self, device_id):
        try:
            self.client.oauth_login(device_id)
        except NotLoggedIn:
            self.client.perform_oauth(open_browser=True)

    def generate_playlist_from_songs(self, songs_ids, playlist_name):
        playlist_id = self.client.create_playlist(playlist_name)
        self.client.add_songs_to_playlist(playlist_id, songs_ids)
