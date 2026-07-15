import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-read-private"
))

user = sp.current_user()
print(f"Connected as: {user['display_name']}")

DB_PATH = "db/spotify.db"
conn = sqlite3.connect(DB_PATH)

top_tracks = pd.read_sql_query("""
    SELECT DISTINCT track_name, artist_name
    FROM streams
    GROUP BY track_name, artist_name
    ORDER BY COUNT(*) DESC
    LIMIT 50
""", conn)

print(f"Top tracks to look up: {len(top_tracks)}")
print(top_tracks.head(10))

def get_track_id(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type="track", limit=1)
    tracks = results["tracks"]["items"]
    if tracks:
        return tracks[0]["id"]
    return None

track_ids = []
for _, row in top_tracks.iterrows():
    track_id = get_track_id(row["track_name"], row["artist_name"])
    track_ids.append(track_id)
    print(f"Found: {row['track_name']} -> {track_id}")

print(f"Track IDs found: {len([t for t in track_ids if t is not None])} out of {len(top_tracks)}")

track_data = []
for i, track_id in enumerate(track_ids):
    if track_id:
        track_info = sp.track(track_id)
        track_data.append({
            "track_name": top_tracks.iloc[i]["track_name"],
            "artist_name": top_tracks.iloc[i]["artist_name"],
            "duration_ms": track_info["duration_ms"],
            "duration_min": round(track_info["duration_ms"] / 60000, 2),
            "explicit": track_info["explicit"],
            "album": track_info["album"]["name"]
        })
        print(f"Got data for: {top_tracks.iloc[i]['track_name']}")

artist_names = top_tracks["artist_name"].unique().tolist()
artist_data = []

for artist_name in artist_names:
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    artists = results["artists"]["items"]
    if artists:
        artist = artists[0]
        artist_data.append({
            "artist_name": artist_name,
            "spotify_id": artist["id"]
        })

tracks_df = pd.DataFrame(track_data)
artists_df = pd.DataFrame(artist_data)

tracks_df.to_csv("exports/track_popularity.csv", index=False)
artists_df.to_csv("exports/artist_data.csv", index=False)

print(f"\nTrack data saved: {len(tracks_df)} tracks")
print(f"Artist data saved: {len(artists_df)} artists")
print("\nSample track data:")
print(tracks_df.head(10).to_string(index=False))