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

## Product Case Studies

Based on patterns found in this data, I wrote two product PRDs proposing 
features Spotify is currently missing:

- **PRD: True Shuffle** - proposes a shuffle toggle with no algorithmic 
weighting, backed by skip rate data showing certain tracks are 
over surfaced while others go unplayed
- **PRD: Spotify Library** - proposes a native library feature that lets 
users build a unified song collection across all their playlists, 
based on a workaround I built myself

Both PRDs are in the docs/ folder.

## Project structure

scripts/01_ingest.py - loads raw JSON into SQLite database
scripts/02_analyze.py - runs analysis queries
scripts/03_export.py - exports CSVs for Power BI

