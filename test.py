import pandas as pd

# URLs to the last three years (2022, 2023, 2024)
urls = [
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2023.parquet",
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.parquet",
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
]

# Load and concatenate into one DataFrame
pbp = pd.concat([pd.read_parquet(url) for url in urls], ignore_index=True)

print("Rows:", len(pbp))
print("Seasons:", pbp['season'].unique())
print(pbp.head())

