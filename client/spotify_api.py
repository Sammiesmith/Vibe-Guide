import requests
import base64
from dotenv import load_dotenv 
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# encode credentials
auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_bytes = auth_string.encode("utf-8")
auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

url = "https://accounts.spotify.com/api/token"

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=data)
token = response.json()["access_token"]

print("Access token:", token)

# get the spotify end point using the access token
def fetch_spotify(endpoint, method="GET", body=None):
    url = f"https://api.spotify.com/{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if method == "GET":
            response = requests.get(url, headers=headers)
    else:
        response = requests.request(method, url, headers=headers, json=body)

    return response.json()


# get user authentication token
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-top-read user-library-read",
            cache_path=".spotify_cache",
            open_browser=True
        )
    )
    return sp



    