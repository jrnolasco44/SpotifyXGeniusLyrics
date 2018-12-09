import os
import json
import spotipy
import requests
import spotipy.util as util
from bs4 import BeautifulSoup


username = '' # spotify username

# Spoitfy Credentials
sp_scope = 'user-read-recently-played user-top-read user-read-playback-state'
sp_client_id = ''
sp_client_secret = ''
sp_redirect_uri = ''

# Genius Credentials
gn_client_id = ''
gn_client_secret = ''
gn_client_token = ''
gn_redirect_uri = ''

try:
    sp_token = util.prompt_for_user_token(
            username=username,
            scope=sp_scope,
            client_id=sp_client_id,
            client_secret=sp_client_secret,
            redirect_uri=sp_redirect_uri
            )
except:
    os.remove(f".cache-{username}")
    sp_token = util.prompt_for_user_token(
            username=username,
            scope=sp_scope,
            client_id=sp_client_id,
            client_secret=sp_client_secret,
            redirect_uri=sp_redirect_uri
            )

# Create Spotify Object
spotifyObject = spotipy.Spotify(auth=sp_token)

user = spotifyObject.current_user()
playback = spotifyObject.currently_playing()

displayName = user['display_name']
numFollowers = user['followers']['total'] # use another bracket to access a lower level of the json response obj

artist_name = playback['item']['artists'][0]['name'] #featuered artists indexed at & after 1
song_title = playback['item']['name']
album_title = playback['item']['album']['name']
album_type = playback['item']['album']['album_type']


print()
print("Welcome to Genius Lyrics, " + displayName + "!")
print()


# METHOD WITH SONG AND ARTIST INPUT
def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + gn_client_token}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

# METHOD TO CRAWL LYRICS
def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

curr_artist = ''
curr_song = ''


# SEARCH FOR MATCHES IN THE REQUEST RESPONSE
response = request_song_info(song_title, artist_name)
json = response.json()
remote_song_info = None

for hit in json['response']['hits']:
    if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
        remote_song_info = hit
        break

# EXTRACT LYRICS FROM URL IF THE SONG WAS FOUND
if remote_song_info:
    song_url = remote_song_info['result']['url']

lyrics = scrap_song_url(song_url)

print()
print('>>>>>>>>>>>> Now playing: ' + song_title + ', by ' + artist_name + ' <<<<<<<<<<<<')
print(lyrics)


# LOOP TO KEEP DISPLAYING LYRICS REAL TIME; MAY TIME OUT

# while True:
#
#     try:
#         playback = spotifyObject.currently_playing()
#     except:
#         pass
#
#     artist_name = playback['item']['artists'][0]['name'] #featuered artists indexed at & after 1
#     song_title = playback['item']['name']
#
#     if curr_artist != artist_name or curr_song != song_title:
#         curr_artist = artist_name
#         curr_song = song_title
#
#         # SEARCH FOR MATCHES IN THE REQUEST RESPONSE
#         response = request_song_info(song_title, artist_name)
#         json = response.json()
#         remote_song_info = None
#
#         for hit in json['response']['hits']:
#             if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
#                 remote_song_info = hit
#                 break
#
#         # EXTRACT LYRICS FROM URL IF THE SONG WAS FOUND
#         if remote_song_info:
#             song_url = remote_song_info['result']['url']
#
#         lyrics = scrap_song_url(song_url)
#
#         print()
#         print('>>>>>>>>>>>> Now playing: ' + song_title + ', by ' + artist_name + ' <<<<<<<<<<<<')
#         print(lyrics)

# TEST PRINT JSON RESPONSES
#print(json.dumps(song_title, sort_keys=True, indent=4))
