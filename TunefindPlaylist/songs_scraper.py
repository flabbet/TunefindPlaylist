import re

import requests
from bs4 import BeautifulSoup

from TunefindPlaylist.song import Song


class SongsScraper:
    season_link_selector = "h3.EpisodeListItem__title___32XUR"
    "div.SongRow__container___3eT_L >  div.SongRow__row___2Bih9 > div.SongRow__center___1HKjk"
    title_selector = "div.SongRow__center___1HKjk .SongTitle__link___2OQHD"
    artist_selector = "div.SongRow__center___1HKjk .Subtitle__subtitle___1rSyh"

    url = None

    def __init__(self, url):
        self.url = url

    def get_songs(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            songs = list()
            doc = BeautifulSoup(response.text, 'html.parser')
            titles = doc.select(self.title_selector)
            artists = doc.select(self.artist_selector)
            for i in range(len(titles)):
                songs.append(Song(titles[i].text, artists[i].text))
            return songs

    def get_songs_ids(self, songs):
        ids = list()
        for song in songs:
            ids.append(self.get_song_id(song))
        return ids

    def get_song_id(self, song: Song):
        resp = requests.get("https://play.google.com/store/search?q={} {}&c=music".format(song.title, song.artist))
        if resp.status_code == 200:
            doc = BeautifulSoup(resp.text, 'html.parser')
            return re.search(r"&tid=song-([\w-]*)",
                             doc.select_one("a > [title=\"{}\"]".format(song.title)).parent['href']).group(1).replace(
                "&tid=song-", "")
