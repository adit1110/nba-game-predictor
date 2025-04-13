import os
import pandas as pd
from glob import glob

# Input/output paths
input_dir = "../data/raw/team_game_logs"
output_dir = "../data/processed/rolling_averages"
os.makedirs(output_dir, exist_ok=True)

# Stats to compute rolling averages for
rolling_stats = ["PTS", "FG_PCT", "AST", "TRB", "TOV"]
windows = [3, 5]  # 3-game and 5-game rolling windows

# Loop through all team gamelogs
for file in glob(os.path.join(input_dir, "*_gamelog.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    try:
        df = pd.read_csv(file)

        # Sort by game date
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
        df = df.sort_values("GAME_DATE").reset_index(drop=True)

        # Add rolling averages
        for stat in rolling_stats:
            if stat not in df.columns:
                continue
            for w in windows:
                df[f"{stat}_avg_{w}"] = df[stat].rolling(window=w, min_periods=1).mean().shift(1)

        # Save to processed folder
        df.to_csv(os.path.join(output_dir, f"{team_abbr}_rolling.csv"), index=False)
        print(f"✅ Processed {team_abbr}")

    except Exception as e:
        print(f"⚠️ Failed to process {team_abbr}: {e}")
