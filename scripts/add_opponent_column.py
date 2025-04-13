import os
import pandas as pd
from glob import glob

# Paths
input_dir = "../data/processed/rolling_averages_with_flags"
output_dir = "../data/processed/rolling_with_flags_and_opp"
os.makedirs(output_dir, exist_ok=True)

# Parse opponent from MATCHUP
def extract_opponent(matchup):
    if "vs." in matchup:
        return matchup.split("vs.")[-1].strip()
    elif "@" in matchup:
        return matchup.split("@")[-1].strip()
    else:
        return "UNKNOWN"

# Loop through all team files
for file in glob(os.path.join(input_dir, "*_rolling_flags.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    try:
        df = pd.read_csv(file)
        df["opponent_abbr"] = df["MATCHUP"].apply(extract_opponent)

        # Save updated file
        output_path = os.path.join(output_dir, f"{team_abbr}_rolling_flags_opp.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Processed {team_abbr}")

    except Exception as e:
        print(f"⚠️ Error processing {team_abbr}: {e}")
