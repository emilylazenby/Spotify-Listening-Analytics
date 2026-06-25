import json
import sqlite3
import os

DATA_DIR = "my_spotify_data/Spotify Account Data"
DB_PATH = "db/spotify.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM streams")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS streams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        end_time TEXT,
        artist_name TEXT,
        track_name TEXT,
        ms_played INTEGER
    )
""")
conn.commit()

music_files = [
    "StreamingHistory_music_0.json",
    "StreamingHistory_music_1.json"
]

records = []

for filename in music_files:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            artist = entry["artistName"].strip()
            track = entry["trackName"].strip()
    
            if not artist or not track:
                continue
            if artist.lower() == "unknown artist" or track.lower() == "unknown track":
                continue
    
            records.append((
                entry["endTime"],
                artist,
                track,
                entry["msPlayed"]
            ))

print(f"Records loaded into memory: {len(records)}")
cursor.executemany("""
    INSERT INTO streams (end_time, artist_name, track_name, ms_played)
    VALUES (?, ?, ?, ?)
""", records)

conn.commit()
conn.close()
print(f"Done. {len(records)} records inserted into the database.")