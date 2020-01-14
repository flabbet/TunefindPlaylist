from gmusicapi.exceptions import InvalidDeviceId

from TunefindPlaylist.playlist_manager import PlaylistManager
from TunefindPlaylist.songs_scraper import SongsScraper


def main():
    scraper = SongsScraper("https://www.tunefind.com/movie/the-app-2019")
    songs = scraper.get_songs()
    songs_ids = scraper.get_songs_ids(songs)
    device_id = input("Specify your device id or click enter and we'll try to get one:")
    try:
        manager = PlaylistManager(device_id)
    except InvalidDeviceId as ex:
        manager = PlaylistManager(ex.valid_device_ids[0])
    manager.generate_playlist_from_songs(songs_ids, "The App")


if __name__ == '__main__':
    main()
