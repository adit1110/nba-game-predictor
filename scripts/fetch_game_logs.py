from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
import pandas as pd
import time
import os

# Constants
SEASON = "2023-24"
SEASON_TYPE = "Regular Season"
SAVE_DIR = os.path.join("..", "data", "raw", "team_game_logs")

# Create directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Get list of all NBA teams
nba_teams = teams.get_teams()

# Loop through each team and fetch game logs
for team in nba_teams:
    team_id = team["id"]
    team_abbr = team["abbreviation"]
    print(f"Fetching logs for {team_abbr}...")

    try:
        log = teamgamelog.TeamGameLog(team_id=team_id, season=SEASON, season_type_all_star=SEASON_TYPE)
        df = log.get_data_frames()[0]

        # Save to CSV in your structure
        csv_path = os.path.join(SAVE_DIR, f"{team_abbr}_gamelog.csv")
        df.to_csv(csv_path, index=False)

        time.sleep(1.5)  # Rate limit

    except Exception as e:
        print(f"Failed for {team_abbr}: {e}")
