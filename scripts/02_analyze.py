import sqlite3
import pandas as pd

DB_PATH = "db/spotify.db"

conn = sqlite3.connect(DB_PATH)

top_artists = pd.read_sql_query("""
    SELECT artist_name,
           COUNT(*) as play_count,
           ROUND(SUM(ms_played) / 60000.0, 1) as minutes_played
    FROM streams
    GROUP BY artist_name
    ORDER BY play_count DESC
    LIMIT 10
""", conn)

print("=== TOP 10 ARTISTS ===")
print(top_artists.to_string(index=False))
top_tracks = pd.read_sql_query("""
    SELECT track_name,
           artist_name,
           COUNT(*) as play_count
    FROM streams
    GROUP BY track_name, artist_name
    ORDER BY play_count DESC
    LIMIT 10
""", conn)

print("\n=== TOP 10 TRACKS ===")
print(top_tracks.to_string(index=False))

by_hour = pd.read_sql_query("""
    SELECT CAST(SUBSTR(end_time, 12, 2) AS INTEGER) as hour,
           COUNT(*) as play_count
    FROM streams
    GROUP BY hour
    ORDER BY hour
""", conn)

print("\n=== PLAYS BY HOUR OF DAY ===")
print(by_hour.to_string(index=False))

by_month = pd.read_sql_query("""
    SELECT SUBSTR(end_time, 1, 7) as month,
           COUNT(*) as play_count,
           ROUND(SUM(ms_played) / 3600000.0, 1) as hours_played
    FROM streams
    GROUP BY month
    ORDER BY month
""", conn)

print("\n=== LISTENING BY MONTH ===")
print(by_month.to_string(index=False))

skip_analysis = pd.read_sql_query("""
    SELECT artist_name,
           COUNT(*) as total_plays,
           SUM(CASE WHEN ms_played < 30000 THEN 1 ELSE 0 END) as skips,
           ROUND(100.0 * SUM(CASE WHEN ms_played < 30000 THEN 1 ELSE 0 END) / COUNT(*), 1) as skip_rate
    FROM streams
    GROUP BY artist_name
    HAVING total_plays >= 20
    ORDER BY skip_rate ASC
    LIMIT 10
""", conn)

print("\n=== MOST LISTENED (LOWEST SKIP RATE) ===")
print(skip_analysis.to_string(index=False))

conn.close()