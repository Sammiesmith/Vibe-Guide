import os
import json
from pathlib import Path

import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from client.spotify_api import get_spotify_client


CACHE_DIR = Path("spotify_local_cache")
CACHE_DIR.mkdir(exist_ok=True)

RAW_JSON_PATH = CACHE_DIR / "recent_liked_tracks.json"
TRACKS_CSV_PATH = CACHE_DIR / "tracks.csv"
TRACK_ARTISTS_CSV_PATH = CACHE_DIR / "track_artists.csv"

# Fetch Liked Tracks
def fetch_recent_liked_tracks(sp, max_tracks=50):
    items = []
    limit = 50
    offset = 0

    while len(items) < max_tracks:
        response = sp.current_user_saved_tracks(limit=limit, offset=offset)
        batch = response.get("items", [])

        if not batch:
            break

        items.extend(batch)
        offset += limit

        print(f"Fetched {min(len(items), max_tracks)} / {max_tracks}")

    return items[:max_tracks]

# Save raw JSON
def save_raw_json(items, path=RAW_JSON_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"Saved raw JSON to {path}")

# Build DataFrame
def build_dataframes(items):

    track_rows = []
    track_artist_rows = []

    for item in items:

        track = item.get("track")
        if not track:
            continue

        album = track.get("album", {})
        artists = track.get("artists", [])

        artist_ids = [a.get("id") for a in artists if a.get("id")]
        artist_names = [a.get("name") for a in artists]

        track_rows.append({
            "added_at": item.get("added_at"),
            "track_id": track.get("id"),
            "track_name": track.get("name"),
            "duration_ms": track.get("duration_ms"),
            "explicit": track.get("explicit"),
            "track_popularity": track.get("popularity"),
            "album_id": album.get("id"),
            "album_name": album.get("name"),
            "album_release_date": album.get("release_date"),
            "artist_ids": artist_ids,
            "artist_names": artist_names,
        })

        for artist in artists:
            track_artist_rows.append({
                "track_id": track.get("id"),
                "track_name": track.get("name"),
                "artist_id": artist.get("id"),
                "artist_name": artist.get("name"),
                "added_at": item.get("added_at"),
            })

    tracks_df = pd.DataFrame(track_rows)
    track_artists_df = pd.DataFrame(track_artist_rows)

    return tracks_df, track_artists_df


# Save Data Frame
def save_dataframes(tracks_df, track_artists_df):

    # always save CSV
    tracks_df.to_csv(TRACKS_CSV_PATH, index=False)
    track_artists_df.to_csv(TRACK_ARTISTS_CSV_PATH, index=False)

    print(f"Saved CSV: {TRACKS_CSV_PATH}")
    print(f"Saved CSV: {TRACK_ARTISTS_CSV_PATH}")


def main():

    sp = get_spotify_client()

    items = fetch_recent_liked_tracks(sp, max_tracks=50)

    save_raw_json(items)

    tracks_df, track_artists_df = build_dataframes(items)

    save_dataframes(tracks_df, track_artists_df)


if __name__ == "__main__":
    main()