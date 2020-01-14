import re

import requests
from bs4 import BeautifulSoup

from TunefindPlaylist.song import Song


class SongsScraper:
    base_url = "https://www.tunefind.com"
    season_link_selector = "h3.EpisodeListItem__title___32XUR > a"
    "div.SongRow__container___3eT_L >  div.SongRow__row___2Bih9 > div.SongRow__center___1HKjk"
    title_selector = "div.SongRow__center___1HKjk .SongTitle__link___2OQHD"
    artist_selector = "div.SongRow__center___1HKjk .Subtitle__subtitle___1rSyh"
    playlist_name_selector = "div.container > h1"
    item_selector = "a[href*='tid']"

    url = None

    def __init__(self, url):
        self.url = url

    def get_playlist_name(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            doc = BeautifulSoup(response.text, 'html.parser')
            return doc.select_one(self.playlist_name_selector).text

    def get_songs(self, url=None):
        if url is None:
            url = self.url
        urls = self.__get_urls_with_songs(url)
        songs = list()
        for current_url in urls:
            response = requests.get(current_url)
            if response.status_code == 200:
                doc = BeautifulSoup(response.text, 'html.parser')
                titles = doc.select(self.title_selector)
                artists = doc.select(self.artist_selector)
                for i in range(len(titles)):
                    song = Song(titles[i].text, artists[i].text)
                    songs.append(song)
                    print("Song found: {} by {}".format(song.title, song.artist))
        return songs

    def __get_urls_with_songs(self, url):
        urls = list()
        response = requests.get(url)
        if response.status_code == 200:
            doc = BeautifulSoup(response.text, 'html.parser')
            if len(doc.select(self.title_selector)) > 0:
                urls.append(url)
            else:
                link_holders = doc.select(self.season_link_selector)
                for link_holder in link_holders:
                    urls.extend(self.__get_urls_with_songs(self.base_url + link_holder['href']))
        return urls


    def get_songs_ids(self, songs):
        ids = list()
        for song in songs:
            print("Getting song id for {} by {}".format(song.title, song.artist))
            song_id = self.get_song_id(song)
            if song_id is not None:
                ids.append(song_id)
        return ids

    def get_song_id(self, song: Song):
        resp = requests.get("https://play.google.com/store/search?q={} {}&c=music".format(song.title, song.artist))
        if resp.status_code == 200:
            doc = BeautifulSoup(resp.text, 'html.parser')
            try:
                return re.search(r"&tid=song-([\w-]*)",
                                 doc.select_one(self.item_selector)['href']).group(1).replace(
                    "&tid=song-", "")
            except TypeError:
                print("{} by {} not found in Google Play Music.".format(song.title, song.artist))
