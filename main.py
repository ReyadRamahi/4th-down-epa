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

user_team = input("Enter a team name: ").upper()

teams_fourth_plays = fourth_down[fourth_down["posteam"] == user_team]


# Helpful data stored in dataframe
#[down, ydstogo, yardline_100, score_differential, yards_gained,
# touchdown, interception, fumble_lost, field_goal_result,
# posteam_score, posteam_score_post, play_type, game_id, drive]

print(f"{user_team} had {len(teams_fourth_plays)} 4th-down plays.")

# Filter to actual 4th-down plays where a conversion could occur
attempts = teams_fourth_plays[
    teams_fourth_plays["play_type"].isin(["pass", "run"])
]

#calculate the conversion rate of fourth downs
conversion_rate = attempts["fourth_down_converted"].mean()

print(f"{user_team} overall 4th-down conversion rate: {conversion_rate:.2%}")

#seperate all of the fourth down plays into drives
drives = teams_fourth_plays.groupby(["game_id", "drive"])

#calculate the 
def epa_from_conversion(yardline_100):
    plays_from_yrd100 = drives.filter(lambda d: d["yardline_100"].min() <= yardline_100)
    drives_from_yrd100 =  plays_from_yrd100.groupby(["game_id", "drive"])
    points_by_drive = (
        drives_from_yrd100["posteam_score_post"].max() -
        drives_from_yrd100["posteam_score"].min()
    )
    avg_points = points_by_drive.mean()
    return avg_points

def opp_team_epa(defteam, yardline_100): 
    opp_team_plays = pbp[pbp["posteam"] == defteam]
    opp_drives = opp_team_plays.groupby(["game_id", "drive"])
    plays_from_yrd100 = opp_drives.filter(lambda d: d["yardline_100"].min() <= yardline_100)

    drives_from_yrd100 =  plays_from_yrd100.groupby(["game_id", "drive"])
    points_by_drive = (
        drives_from_yrd100["posteam_score_post"].max() -
        drives_from_yrd100["posteam_score"].min()
    )
    avg_points = points_by_drive.mean()
    return avg_points


def calculate_epa(play):
    ytg = play["ydstogo"]
    yl  = play["yardline_100"]
    dft = play["defteam"]

    conversion_rate_yds_to_go = attempts.loc[
        (attempts["ydstogo"] >= ytg - 1) & 
        (attempts["ydstogo"] <= ytg + 1),
        "fourth_down_converted"
    ].mean()

    team_ep = epa_from_conversion(yl)
    opp_ep  = opp_team_epa(dft, yl)

    epa_of_play = (conversion_rate_yds_to_go * team_ep) - opp_ep
    return epa_of_play

# Iterate through all 4th-down plays for the chosen team
# and calculate the EPA for each
teams_fourth_plays["calc_epa"] = teams_fourth_plays.apply(calculate_epa, axis=1)

# Identify plays where the math says "go for it" but they didn't
should_have_gone = teams_fourth_plays[
    (teams_fourth_plays["calc_epa"] > 0) &
    (teams_fourth_plays["play_type"].isin(["punt", "field_goal"]))
]

# Print the summary
print(f"{user_team} should have gone for it on {len(should_have_gone)} plays.")

# Show the key details of those plays
print(should_have_gone[[
    "game_id", "qtr", "time", "ydstogo", "yardline_100", "play_type", "desc", "calc_epa"
]])






