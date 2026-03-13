import pandas as pd
from pathlib import Path


CACHE_DIR = Path("spotify_local_cache")

TRACKS_PATH = CACHE_DIR / "tracks.csv"
TRACK_ARTISTS_PATH = CACHE_DIR / "track_artists.csv"


def load_data():

    tracks_df = pd.read_csv(TRACKS_PATH)
    track_artists_df = pd.read_csv(TRACK_ARTISTS_PATH)

    return tracks_df, track_artists_df


def most_common_artists(track_artists_df):

    print("\nMost common artists:\n")

    print(
        track_artists_df["artist_name"]
        .value_counts()
        .head(10)
    )


def most_common_albums(tracks_df):

    print("\nMost common albums:\n")

    print(
        tracks_df["album_name"]
        .value_counts()
        .head(10)
    )


def lowest_popularity(tracks_df):

    print("\nLeast popular tracks:\n")

    print(
        tracks_df[["track_name", "track_popularity"]]
        .sort_values("track_popularity")
        .head(10)
    )


def main():

    tracks_df, track_artists_df = load_data()

    most_common_artists(track_artists_df)

    most_common_albums(tracks_df)

    lowest_popularity(tracks_df)


if __name__ == "__main__":
    main()