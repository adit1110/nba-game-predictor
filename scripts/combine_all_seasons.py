import os
import pandas as pd
from glob import glob

input_dir = "../data/raw/team_game_logs_multi"
output_file = "../data/raw/team_gamelogs_all_seasons.csv"

# Load all gamelogs
all_files = glob(os.path.join(input_dir, "*_gamelog.csv"))
all_logs = []

for file in all_files:
    try:
        df = pd.read_csv(file)
        team_abbr = os.path.basename(file).split("_")[0]
        df["team_abbr"] = team_abbr
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
        all_logs.append(df)
    except Exception as e:
        print(f"⚠️ Error reading {file}: {e}")

# Combine all into one DataFrame
combined_df = pd.concat(all_logs, ignore_index=True)

# Save unified file
combined_df.to_csv(output_file, index=False)
print(f"✅ Unified dataset saved to {output_file}")
print(f"Total games: {len(combined_df)}")
