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
    scraper = SongsScraper(sys.argv[1])
    playlist_name = scraper.get_playlist_name()
    songs = scraper.get_songs()
    songs_ids = scraper.get_songs_ids(songs)
    try:
        manager = PlaylistManager(device_id)
    except InvalidDeviceId as ex:
        manager = PlaylistManager(ex.valid_device_ids[0])
    manager.generate_playlist_from_songs(songs_ids, playlist_name)
    print("\nDone! Playlist was saved as '{}'".format(playlist_name))


if __name__ == '__main__':
    main()
