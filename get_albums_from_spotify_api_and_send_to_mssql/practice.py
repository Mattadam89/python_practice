import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd

# # load environment variables
# load_dotenv()

# scope = 'playlist-read-private'

# # construct spotify client credentials object, clientid and secret passed
# # automatically via environment variables
# auth_manager = SpotifyOAuth(scope = scope)
# sp = spotipy.Spotify(auth_manager=auth_manager)

# with open('artist_details.json', 'r') as file:
#     data = json.load(file)

# print(len(data))


# Load JSON data into a DataFrame
df = pd.read_json('artist_details.json')

# Convert DataFrame to CSV
df.to_csv("output.csv", index=False)