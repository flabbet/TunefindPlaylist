import sys

from gmusicapi.exceptions import InvalidDeviceId

from TunefindPlaylist.playlist_manager import PlaylistManager
from TunefindPlaylist.songs_scraper import SongsScraper


def main():
    device_id = ""
    if len(sys.argv) < 2:
        print("Please provide an URL. (example. TunefindPlaylist https://www.tunefind.com/show/derry-girls)")
        return
    if len(sys.argv) >= 3:
        device_id = sys.argv[2]

    try:
        manager = PlaylistManager(device_id)
    except InvalidDeviceId as ex:
        try:
            manager = PlaylistManager(ex.valid_device_ids[0])
        except IndexError:
            print("Didn't found valid device.")
            return

    if not manager.client.is_authenticated():
        print("Login failed")
        return

    if not manager.client.is_subscribed:
        print("This account plan is too weak. Please upgrade your subscription in Google Play Store.")
        return

    scraper = SongsScraper(sys.argv[1])
    playlist_name = scraper.get_playlist_name()
    songs = scraper.get_songs()
    songs_ids = scraper.get_songs_ids(songs)
    manager.generate_playlist_from_songs(songs_ids, playlist_name)
    print("\nDone! Playlist was saved as '{}'".format(playlist_name))


if __name__ == '__main__':
    main()
