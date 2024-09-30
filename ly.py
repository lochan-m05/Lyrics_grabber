import os
import time
import spotipy
import lyricsgenius as lg

#Spotify and Genius API credentials
spotipy_client_id = 'b4a7b20e1b134598aea09cae9b0ec44e'
spotipy_client_secret = '8b6dd42c81cb47989d6cc2c223db3d54'
spotipy_redirect_uri = 'https://www.google.com/'  # Should be the actual registered redirect URI
genius_access_token = os.environ.get('GENIUS_ACCESS_TOKEN')  # Ensure this is set in the environment

# Scope for Spotify (to read currently playing song)
scope = 'user-read-currently-playing'

# OAuth object creation for Spotify
oauth_object = spotipy.SpotifyOAuth(
    client_id=spotipy_client_id,
    client_secret=spotipy_client_secret,
    redirect_uri=spotipy_redirect_uri,
    scope=scope,
    cache_path=r"E:\Python\.cache"
)

# refresh the Spotify token
def get_spotify_token(oauth):
    token_dict = oauth.get_cached_token()
    
    #  request a new one
    if token_dict is None:
        print("No cached token found. Redirecting to Spotify login for authorization.")
        token_dict = oauth.get_access_token()
    
    # Return the token if available
    if token_dict and 'access_token' in token_dict:
        return token_dict['access_token']
    else:
        raise Exception("Failed to retrieve access token.")

#  currently playing song
def get_current_song(spotify_obj):
    try:
        current_song = spotify_obj.currently_playing()
        if current_song is None or current_song.get('item') is None:
            return None, None
        artist_name = current_song['item']['album']['artists'][0]['name']
        song_title = current_song['item']['name']
        return artist_name, song_title
    except Exception as e:
        print(f"Error fetching current song: {e}")
        return None, None

#  to fetch lyrics 
def fetch_song_lyrics(genius_obj, song_title, artist_name):
    try:
        song = genius_obj.search_song(title=song_title, artist=artist_name)
        if song:
            return song.lyrics
        else:
            return "Lyrics not found on Genius."
    except Exception as e:
        return f"Error fetching lyrics: {e}"

#  monitor currently playing
def monitor_playing_song(spotify_obj, genius_obj):
    previous_song_title = None
    previous_artist_name = None

    while True:
        artist_name, song_title = get_current_song(spotify_obj)

        if artist_name is None or song_title is None:
            print("No song playing or ad detected. Sleeping for 40 seconds...")
            time.sleep(40)  # Sleep when no song is playing
        else:
            #  fetch the new lyrics
            if song_title != previous_song_title or artist_name != previous_artist_name:
                print(f"Song changed to: {song_title} by {artist_name}")
                lyrics = fetch_song_lyrics(genius_obj, song_title, artist_name)
                print(lyrics)
                # Update previous song and artist
                previous_song_title = song_title
                previous_artist_name = artist_name

        
        time.sleep(10)

# Main function 
def main():
    try:
        # Get Spotify token
        oauth = get_spotify_token(oauth_object)
        
        # Create Spotify and Genius API objects
        spotify_object = spotipy.Spotify(auth=oauth)
        genius_object = lg.Genius(genius_access_token)

        # Start monitoring currently playing song
        monitor_playing_song(spotify_object, genius_object)
    
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
