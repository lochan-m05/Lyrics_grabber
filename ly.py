
# import all the imp lib
import os
import json
import time
import spotipy
import lyricsgenius as lg

# store the env varlable
spotipy_client_id = 'b4a7b20e1b134598aea09cae9b0ec44e'
spotipy_client_secret = '8b6dd42c81cb47989d6cc2c223db3d54'
spotipy_redirect_uri = 'https://www.google.com/'
genius_access_token = os.environ.get('GENIUS_ACCESS_TOKEN')

# scope is used to read the currently playing song 
scope = 'user-read-currently-playing'

#OAuth object creation
oauth_object = spotipy.SpotifyOAuth(client_id=spotipy_client_id,
                                    client_secret=spotipy_client_secret,
                                    redirect_uri=spotipy_redirect_uri,
                                    scope=scope ,
                                    cache_path="E:Python/.cache")

# Get the access token (use the cached token if available)
token_dict = oauth_object.get_cached_token()
token=token_dict['access_token']

if token_dict is None:
    print("No cached token found redirecting to Spotify login for authorization")
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']


#create spotipy and genius object
spotipy_object = spotipy.Spotify(auth=token)
genius_object = lg.Genius(genius_access_token)

#set previous_song_title to null
previous_song_title = None
previous_artist_name = None

#loop
while True:
    current = spotipy_object.currently_playing()

    
    if current is None or current.get('item') is None:
        print("An ad is playing. Sleeping for 40 seconds...")
        time.sleep(40)  
    else:
      
        artist_name = current['item']['album']['artists'][0]['name']
        song_title = current['item']['name']

  
        if song_title != previous_song_title or artist_name != previous_artist_name:
            print(f"Song changed to: {song_title} by {artist_name}")
            
           
            song = genius_object.search_song(title=song_title, artist=artist_name)
            
           
            if song:
                lyrics = song.lyrics
                print(lyrics)
            else:
                print("Song not found on Genius.")
            
      
            previous_song_title = song_title
            previous_artist_name = artist_name
        else:
            print()


    time.sleep(10)
