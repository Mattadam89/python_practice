import SpotifyAPIFunctions
import json
import pandas as pd

# Get list of all my playlists
playlists = SpotifyAPIFunctions.get_my_playlists()

## Get a list of all the tracks in my playlists
playlists_tracks = SpotifyAPIFunctions.get_all_playlists_and_tracks(playlists)

## Get a list of the artists spotify IDs associcated with all the tracks in my playlists
artists_ids = SpotifyAPIFunctions.get_artists_from_tracks(playlists_tracks)

## Get the details of all the artists appearing in my playlists
artists_details = SpotifyAPIFunctions.get_artist_detail(artists_ids)

## Create a list of dictionaries for each artist id and genre combination
artist_id_genres = SpotifyAPIFunctions.flatten_artist_id_genres_dict(artists_details)

## Output required data to CSV for ingestion by SSIS package
df = pd.DataFrame.from_dict(playlists)
df.to_csv("playlists.csv", index=False)

df = pd.DataFrame.from_dict(playlists_tracks)
df.to_csv("playlists_tracks.csv", index=False)

df = pd.DataFrame.from_dict(artists_details)
df.to_csv("artists_details.csv", index=False)

df = pd.DataFrame.from_dict(artist_id_genres)
df.to_csv("artist_id_genres.csv", index=False)