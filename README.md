# Spotify Listening Analytics

A personal data analytics project built on one year of Spotify streaming history 
(June 2025 to June 2026).

## What this project does

- Ingests raw JSON data from Spotify's personal data export into a SQLite database
- Runs SQL queries via Python to analyze listening patterns
- Exports clean CSVs for visualization
- Visualizes findings in a Power BI dashboard

## Tools used

- Python 
- SQLite
- Power BI

## Key findings

- Top artist: The Haunt (229 plays, 400 minutes)
- Most played track: obsessed
- Peak listening hours: midnight to 5am and 10pm to 11pm
- Highest listening month: July 2025 (51 hours)
- Most loyal artist by skip rate: Florence + The Machine (4.9% skip rate)

## Project structure

scripts/01_ingest.py - loads raw JSON into SQLite database
scripts/02_analyze.py - runs analysis queries
scripts/03_export.py - exports CSVs for Power BI

## Updates

- Corrected listening hours from UTC to CST (5 hour offset applied in export)
- Top tracks now display as "track (artist)" for clearer identification
