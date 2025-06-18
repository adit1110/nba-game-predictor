# add_player_level_features.py
import os
import pandas as pd
from glob import glob

# Paths
team_data_path = "../data/processed/final_training_data.csv"
player_logs_dir = "../data/raw/player_game_logs"
output_path = "../data/processed/final_training_data_with_players.csv"

# Load team data
team_df = pd.read_csv(team_data_path)
team_df["GAME_DATE"] = pd.to_datetime(team_df["GAME_DATE"])

# Placeholder for new features
team_df["top3_avg_pts"] = 0.0
team_df["top3_avg_ast"] = 0.0
team_df["missing_top_player"] = 0

# Load all player logs
player_dfs = []
for file in glob(os.path.join(player_logs_dir, "*.csv")):
    try:
        df = pd.read_csv(file)
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
        df["PLAYER_NAME"] = os.path.basename(file).replace(".csv", "").replace("_", " ")
        # Extract TEAM_ABBREVIATION from MATCHUP string
        if "MATCHUP" in df.columns:
            df["TEAM_ABBREVIATION"] = df["MATCHUP"].str.extract(r"^([A-Z]{2,3}) ")
        player_dfs.append(df)
    except:
        continue

if not player_dfs:
    raise RuntimeError("❌ No player logs were loaded. Check your internet connection or NBA API access.")

players_df = pd.concat(player_dfs, ignore_index=True)

if "TEAM_ABBREVIATION" not in players_df.columns:
    raise KeyError("❌ 'TEAM_ABBREVIATION' column not found in player data even after extraction. Check log formats.")

# Merge logic
for i, row in team_df.iterrows():
    team = row["Team"]
    game_date = row["GAME_DATE"]

    # Get players who played for that team on that date
    players_in_game = players_df[(players_df["TEAM_ABBREVIATION"] == team) & (players_df["GAME_DATE"] == game_date)]

    if len(players_in_game) == 0:
        team_df.at[i, "missing_top_player"] = 1
        continue

    # Top 3 by MIN or PTS
    top_players = players_in_game.sort_values("MIN", ascending=False).head(3)
    team_df.at[i, "top3_avg_pts"] = top_players["PTS"].mean()
    team_df.at[i, "top3_avg_ast"] = top_players["AST"].mean()

# Save updated dataset
team_df.to_csv(output_path, index=False)
print("✅ Player-level features added and saved to final_training_data_with_players.csv")