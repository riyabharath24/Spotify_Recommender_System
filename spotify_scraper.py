# importing the libraries
import csv
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_FILE_NAME = "song_info.csv"

PLAYLIST_LINK = 'https://open.spotify.com/playlist/37i9dQZF1EVHGWrwldPRtj?si=01fc2bf705074cd2'

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# authenticate


def get_playlist_data(PLAYLIST_LINK, client_credentials_manager):

    session = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError(
            "Expected format: https://open.spotify.com/playlist/...")

    tracks = session.playlist_tracks(playlist_uri)["items"]

    # create csv file
    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(['artist_name', 'track_name', 'album_name',
                        'genres', 'song_popularity', 'artist_popularity'])

        # extract name and artist
        for track in tracks:
            name = track['track']['name']
            artists = ", ".join([artist["name"]
                                for artist in track["track"]["artists"]])

            album = track['track']['album']['name']
            for t in track['track']['artists']:
                artist_uri = t["uri"]

                artist_info = session.artist(artist_uri)
                artist_genres = artist_info["genres"]
                artist_pop = artist_info["popularity"]
                genres = artist_genres

            track_pop = track['track']['popularity']

            writer.writerow(
                [artists, name, album, genres, track_pop, artist_pop])

    return file


get_playlist_data(PLAYLIST_LINK, client_credentials_manager)
print('file generated: {}'.format(OUTPUT_FILE_NAME))
