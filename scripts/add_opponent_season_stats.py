import os
import pandas as pd
from glob import glob

# Paths
input_dir = "../data/processed/rolling_with_flags_and_opp"
output_dir = "../data/processed/enriched"
season_avg_path = "../data/raw/team_averages_from_gamelogs.csv"
os.makedirs(output_dir, exist_ok=True)

# Load team-wide season averages
season_df = pd.read_csv(season_avg_path)
season_df.columns = [col.replace("FG_PCT", "FG%").replace("REB", "TRB") for col in season_df.columns]
season_df = season_df.set_index("Team")

# Columns to pull from opponent
stat_cols = ["AST", "TRB", "FG%", "TOV"]

# Process each file
for file in glob(os.path.join(input_dir, "*_rolling_flags_opp.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    try:
        df = pd.read_csv(file)

        for stat in stat_cols:
            df[f"{stat}_avg_season"] = season_df.loc[team_abbr, stat]
            df[f"opp_{stat}_avg_season"] = df["opponent_abbr"].map(season_df[stat])

        # Save to enriched folder
        out_path = os.path.join(output_dir, f"{team_abbr}_enriched.csv")
        df.to_csv(out_path, index=False)
        print(f"✅ Added opponent season stats to {team_abbr}")

    except Exception as e:
        print(f"⚠️ Error with {team_abbr}: {e}")
