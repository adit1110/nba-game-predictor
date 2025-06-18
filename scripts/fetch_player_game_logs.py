# fetch_player_game_logs.py
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import os
import time

SEASON = "2023-24"
SEASON_TYPE = "Regular Season"
SAVE_DIR = os.path.join("..", "data", "raw", "player_game_logs")
os.makedirs(SAVE_DIR, exist_ok=True)

# Get all players
all_players = players.get_active_players()

for p in all_players:
    player_name = p["full_name"]
    player_id = p["id"]
    print(f"Fetching logs for {player_name}...")

    try:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=SEASON, season_type_all_star=SEASON_TYPE)
        df = gamelog.get_data_frames()[0]

        # Save
        player_file = os.path.join(SAVE_DIR, f"{player_name.replace(' ', '_')}.csv")
        df.to_csv(player_file, index=False)
        time.sleep(1.2)  # To avoid rate limits

    except Exception as e:
        print(f"Failed for {player_name}: {e}")