from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
import pandas as pd
import time
import os

# Config
seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24"]
output_dir = "../data/raw/team_game_logs_multi"
os.makedirs(output_dir, exist_ok=True)

# Get all NBA teams
nba_teams = teams.get_teams()

# Loop through teams + seasons
for team in nba_teams:
    team_abbr = team['abbreviation']
    team_id = team['id']

    for season in seasons:
        try:
            print(f"Fetching {team_abbr} for {season}...")
            logs = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season')
            df = logs.get_data_frames()[0]
            df["TEAM_ABBR"] = team_abbr
            df["SEASON"] = season

            # Save CSV
            file_path = os.path.join(output_dir, f"{team_abbr}_{season.replace('-', '')}_gamelog.csv")
            df.to_csv(file_path, index=False)

            time.sleep(1.2)  # avoid rate limiting

        except Exception as e:
            print(f"⚠️ Failed to fetch {team_abbr} {season}: {e}")
