import os
import pandas as pd
from glob import glob

# Paths
input_dir = "../data/processed/enriched_with_opp_rolling"
output_dir = "../data/processed/contextualized"
os.makedirs(output_dir, exist_ok=True)

# Process each team's enriched game log
for file in glob(os.path.join(input_dir, "*_enriched_opp_rolling.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    try:
        df = pd.read_csv(file)
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

        # Sort by date to compute sequential features
        df = df.sort_values("GAME_DATE").reset_index(drop=True)

        # Initialize new columns
        win_streak = 0
        prev_date = None
        rest_days = []
        b2b_flags = []
        streaks = []

        for i, row in df.iterrows():
            # Win streak
            if row["WL"] == "W":
                win_streak += 1
            else:
                win_streak = 0
            streaks.append(win_streak)

            # Rest days
            if prev_date is not None:
                delta = (row["GAME_DATE"] - prev_date).days
            else:
                delta = None
            rest_days.append(delta)

            # Back-to-back
            b2b_flags.append(1 if delta == 0 else 0)

            # Update previous game date
            prev_date = row["GAME_DATE"]

        df["win_streak"] = streaks
        df["rest_days"] = rest_days
        df["back_to_back"] = b2b_flags

        # Save updated DataFrame
        output_path = os.path.join(output_dir, f"{team_abbr}_final.csv")
        df.to_csv(output_path, index=False)
        print(f"Added context features to {team_abbr}")

    except Exception as e:
        print(f"Error processing {team_abbr}: {e}")
