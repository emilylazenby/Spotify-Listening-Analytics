import sqlite3
import pandas as pd
import os

DB_PATH = "db/spotify.db"
EXPORT_DIR = "exports"

os.makedirs(EXPORT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

pd.read_sql_query("""
    SELECT artist_name,
           COUNT(*) as play_count,
           ROUND(SUM(ms_played) / 60000.0, 1) as minutes_played
    FROM streams
    WHERE artist_name != 'Unknown Artist'
    GROUP BY artist_name
    ORDER BY play_count DESC
""", conn).to_csv(f"{EXPORT_DIR}/top_artists.csv", index=False)

pd.read_sql_query("""
    SELECT track_name, artist_name,
           COUNT(*) as play_count,
           ROUND(SUM(ms_played) / 60000.0, 1) as minutes_played
    FROM streams
    WHERE artist_name != 'Unknown Artist'
    GROUP BY track_name, artist_name
    ORDER BY play_count DESC
""", conn).to_csv(f"{EXPORT_DIR}/top_tracks.csv", index=False)

pd.read_sql_query("""
    SELECT CAST(SUBSTR(end_time, 12, 2) AS INTEGER) as hour,
           COUNT(*) as play_count
    FROM streams
    GROUP BY hour
    ORDER BY hour
""", conn).to_csv(f"{EXPORT_DIR}/by_hour.csv", index=False)

pd.read_sql_query("""
    SELECT SUBSTR(end_time, 1, 7) as month,
           COUNT(*) as play_count,
           ROUND(SUM(ms_played) / 3600000.0, 1) as hours_played
    FROM streams
    GROUP BY month
    ORDER BY month
""", conn).to_csv(f"{EXPORT_DIR}/by_month.csv", index=False)

conn.close()
print("Exports complete. Check your exports/ folder.")