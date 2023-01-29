import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID= "add your client id"
SPOTIPY_CLIENT_SECRET = "add client secret"
redirect_url = "https://google.com"
scope = "playlist-modify-public"
username = "add username"

auth_manager = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, redirect_url, scope=scope, username=username)
spotify = spotipy.Spotify(auth_manager=auth_manager)
list_of_songs = []


def is_valid_date(date_string):
    match = re.match("\d{4}-\d{2}-\d{2}", date_string)
    if not match:
        return False
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def create_playlist(song_titles, playlist_date):
    playlist = ""
    spotify.user_playlist_create(user=username, name=playlist_date, description="ABC", public=True)
    print("List created")
    for title in song_titles:
        results = spotify.search(q=title)
        list_of_songs.append(results['tracks']['items'][0]['uri'])
        a = 1
        pre_playlists = spotify.user_playlists(user=username)
        playlist = pre_playlists['items'][0]['id']
    spotify.user_playlist_add_tracks(user=username,playlist_id=playlist, tracks=list_of_songs)


date_of_music = input("Please enter the date you want to get music of? Format should be YYYY-MM-DD: ")
if is_valid_date(date_of_music):
    response = requests.get(f'https://www.billboard.com/charts/hot-100/{date_of_music}')
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = [a.text.strip().replace('\n', '').replace('\t', '') for a in soup.select(".o-chart-results-list__item h3#title-of-a-story")]
        # print(titles[:100])
        create_playlist(titles, date_of_music)
    else:
        print("Failed to fetch data from the URL")
else:
    print("Date is not correct")

