from albums_script import get_albums_for_artist
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

print(get_albums_for_artist(artist_id))