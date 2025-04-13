import os
import pandas as pd
from glob import glob

# Paths
input_dir = "../data/processed/rolling_averages"
output_dir = "../data/processed/rolling_averages_with_flags"
os.makedirs(output_dir, exist_ok=True)

# Process each rolling average file
for file in glob(os.path.join(input_dir, "*_rolling.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    try:
        df = pd.read_csv(file)

        # Add is_home flag
        df["is_home"] = df["MATCHUP"].apply(lambda x: 1 if "vs." in x else 0)

        # Save enhanced version
        df.to_csv(os.path.join(output_dir, f"{team_abbr}_rolling_flags.csv"), index=False)
        print(f"✅ Added is_home flag for {team_abbr}")

    except Exception as e:
        print(f"⚠️ Error processing {team_abbr}: {e}")
