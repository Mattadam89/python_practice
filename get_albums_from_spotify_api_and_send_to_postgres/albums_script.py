import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

# load environment variables
load_dotenv()

# construct spotify client credentials object, clientid and secret passed
# automatically via environment variables
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

artist_id = '1qqdO7xMptucPDMopsOdkr'

def get_albums_for_artist(artist_id):
    """Gets all the albums for a given artist id and returns a list of dicts
    with artist name, album name, album ID and release date"""
    # get albums for artist
    albums = []
    offset = 0
    page = 1
    while True:
        artist_name = sp.artist(artist_id)["name"]
        album_results = sp.artist_albums(artist_id, album_type='album', 
                                         offset = offset)
        print(f"Getting page {page} of albums by {artist_name}...")
        albums.extend(
        {"Album ID": item["id"],
         "Album Name": item["name"],
         "Artist ID": artist_id,
         "Artist Name": artist_name,         
         "Release Date": item["release_date"]} for item in album_results["items"])

        if album_results["next"]:
            offset += album_results["limit"]
            page += 1
        else: 
            break
    
    return albums

def get_tracks_from_album(album_id):
    """Gets all the albums for a given album id and returns a list of dicts
    with track id, track title and album id"""
    album_tracks = []
    offset = 0
    while True:
        results = sp.album_tracks(album_id, offset = offset)

        album_tracks.extend(
        {"Track ID": item["id"],
         "Title": item["name"],
         "Album ID": album_id} for item in results["items"])
        
        if results["next"]:
            offset += results["limit"]
        else:
            break

    return album_tracks


# define connection string for sql server
connection_string = (f"mssql+pyodbc://{os.environ["UID"]}:"
                     f"{os.environ["PWD"]}@"
                     f"{os.environ["SERVER"]}/"
                     f"{os.environ["DATABASE"]}?"
                     "driver=ODBC+Driver+17+for+SQL+Server")

# open connection to sql server

def write_albums_and_tracks_to_sql_server(artist_id):
    """
    """
    connection_string = (f"mssql+pyodbc://{os.environ["UID"]}:"
                         f"{os.environ["PWD"]}@"
                         f"{os.environ["SERVER"]}/"
                         f"{os.environ["DATABASE"]}?"
                         "driver=ODBC+Driver+17+for+SQL+Server")
    
    engine = create_engine(connection_string)
    
    artist_albums = get_albums_for_artist(artist_id)

    artist_tracks = []

    for album in artist_albums:
        album_tracks = get_tracks_from_album(album["Album ID"])
        print(f"Getting all the tracks from the album {album["Album Name"]}...")

        #add all the track dicts one by one to the artist tracks list
        artist_tracks.extend(track for track in album_tracks)
    
        
    # artist albums dataframe transformations
    df_artist_albums = pd.DataFrame(artist_albums)
    df_artist_albums['Release Date'] = pd.to_datetime(
                                        df_artist_albums['Release Date'])
    df_artist_albums['updated_at'] = datetime.now()

    # artist tracks dataframe transformations
    df_artist_tracks = pd.DataFrame(artist_tracks)
    df_artist_tracks['updated_at'] = datetime.now()

    # write dataframes to MSSQL
    df_artist_albums.to_sql("artist_albums", engine, 
                            schema= "dbo", if_exists= 'replace',
                            index = False)
    
    df_artist_tracks.to_sql("album_tracks", engine, 
                            schema= "dbo", if_exists= 'replace', 
                            index = False)
    
write_albums_and_tracks_to_sql_server(artist_id)
    
    












