import spotipy
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# load environment variables
load_dotenv()

scope = 'playlist-read-private'

# construct spotify client credentials object, clientid and secret passed
# automatically via environment variables
auth_manager = SpotifyOAuth(scope = scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_my_playlists():
    """Gets all of my playlists"""
    playlists_dict = []
    offset = 0
    page = 1
    limit = 50
    print("Getting playlists IDs")
    while True:

        results = sp.current_user_playlists(limit=limit, offset=offset)
        
        playlists_dict.extend(
            {
                "Update Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Playlist ID": item["id"],
                "Playlist Name": item["name"]
            } 
            for item in results["items"]
        )

        if results["next"]:
            offset += limit
            page += 1
        else:
            break    
    print("Finshed capturing playlist IDs")
    return playlists_dict

def get_tracks_from_playlist(playlist_id):
    tracks_dict = []
    offset = 0
    page = 1
    limit = 50
    print("Getting tracks from Playlists")
    while True:

        results = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        
        tracks_dict.extend(
            {
                "Update Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Track ID": item["track"]["id"],
                "Title": item["track"]["name"],
                "Playlist ID": playlist_id, 
                "Artist ID": ",".join(artists["id"] for artists in item["track"]["artists"])
            } 
            for item in results["items"]
        )

        if results["next"]:
            offset += limit
            page += 1
        else:
            break
    
    print("Finshed capturing tracks from playlists")
    
    return tracks_dict

def get_artist_detail(artist_id_list):

    artist_id_list = artist_id_list
    artist_details = []
    print(f"Getting details for {len(artist_id_list)} artists..")

    while artist_id_list:
        print(f"Getting details for next {len(artist_id_list[0:50])} artists")
        results = sp.artists(artist_id_list[0:50])
        del artist_id_list[0:50]

        artist_details.extend (
            {
                "Update Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Artist ID": artist["id"],
                "Name": artist["name"],
                "Genre": artist["genres"]
            }
            for artist in results["artists"]
        )

    return artist_details



def get_all_playlists_and_tracks(playlists_dict):

    playlists_tracks = [tracks for playlist in playlists_dict for tracks in get_tracks_from_playlist(playlist["Playlist ID"])]    

    return playlists_tracks

def get_artists_from_tracks(tracks_dicts):

    artist_ids_list = list(set([artist_id for track_dict in tracks_dicts for artist_id in track_dict["Artist ID"].split(',')]))

    print("List of Artist ID's captured")

    return artist_ids_list

def flatten_artist_id_genres_dict(artists_details_dict):
    """ Flattens a list of dictionaries where each dictionary has a key value
     pair of artist id and genres where each genre value is a list of 1 or more
       strings """
    artist_id_genre = []
    
    artist_id_genre.extend(
        {
            "Update Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Artist ID": artist["Artist ID"],
            "Genre": genre
        }        
        for artist in artists_details_dict for genre in artist["Genre"]
    )

    return artist_id_genre

def write_to_json(dict, filename):
    json_file = json.dumps(dict, indent = 4)

    with open(f"{filename}.json", "w") as jsonfile:
        jsonfile.write(json_file)

