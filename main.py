import pandas as pd

# URLs to the last three years (2022, 2023, 2024)
urls = [
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2023.parquet",
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.parquet",
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
]

# Load and concatenate into one DataFrame
pbp = pd.concat([pd.read_parquet(url) for url in urls], ignore_index=True)

fourth_down = pbp[pbp["down"] == 4]

team = input("Enter a team name: ").upper()

teams_fourth_plays = fourth_down[fourth_down["posteam"] == team]


# Helpful data stored in dataframe
#[down, ydstogo, yardline_100, score_differential, yards_gained,
# touchdown, interception, fumble_lost, field_goal_result,
# posteam_score, posteam_score_post, play_type, game_id, drive]

print(f"{team} had {len(teams_fourth_plays)} 4th-down plays.")

# Filter to actual 4th-down plays where a conversion could occur
attempts = teams_fourth_plays[
    teams_fourth_plays["play_type"].isin(["pass", "run"])
]

conversion_rate = attempts["fourth_down_converted"].mean()

print(f"{team} overall 4th-down conversion rate: {conversion_rate:.2%}")

drives = teams_fourth_plays.groupby(["game_id", "drive"])

def calculate_epa(play):
    conversion_rate_yds_to_go = attempts["ydstogo" == play.ydstogo + 1 | "ydstogo" == play.ydstogo | "ydstogo" == play.ydstogo - 1].mean()
    epa_in_poss = conversion_rate_yds_to_go *  
    return epa_value

