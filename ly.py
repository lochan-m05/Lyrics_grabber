import os
import json
import time
import spotipy
import lyricsgenius as lg

# Environment variables for Spotipy and Genius credentials
spotipy_client_id = os.environ['SPOTIPY_CLIENT_ID']
spotipy_client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
spotipy_redirect_uri = os.environ['SPOTIPY_REDIRECT_URl']
genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']

# Scope for Spotify API to read currently playing track
scope = 'user-read-currently-playing'

# Spotify OAuth object creation
oauth_object = spotipy.SpotifyOAuth(client_id=spotipy_client_id,
                                    client_secret=spotipy_client_secret,
                                    redirect_uri=spotipy_redirect_uri,
                                    scope=scope,
                                    cache_path="E:Python/.cache" )

# Get access token
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']


# Create Spotify and Genius API objects
spotipy_object = spotipy.Spotify(auth=token)
genius_object = lg.Genius(genius_access_token)


while True:
    current = spotipy_object.currently_playing()
    status = current['currently_playing_type']

    if status == 'track' :
        artist_name = current['item']['album']['artists'][0]['name']
        song_title = current['item']['name']
    
        length =  current['item']['duration_ms']
        progress = current['progress_ms']
        time_ms = length - progress
        elapsed_time = int((time_ms / 1000))


        song = genius_object.search_song(title=song_title, artist=artist_name)
        lyrics = song.lyrics
        print("\n",lyrics)

        time.sleep(elapsed_time)
     
     
    elif status == 'ad' :
        time.sleep(30)




