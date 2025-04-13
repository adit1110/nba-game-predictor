import os
import pandas as pd
from glob import glob

# Directories
input_dir = "../data/processed/enriched"
opponent_dir = "../data/processed/rolling_with_flags_and_opp"
output_dir = "../data/processed/enriched_with_opp_rolling"
os.makedirs(output_dir, exist_ok=True)

# Identify rolling stat columns from opponent files
sample_team = "BKN"
sample_file = os.path.join(opponent_dir, f"{sample_team}_rolling_flags_opp.csv")
sample_df = pd.read_csv(sample_file)
rolling_cols = [col for col in sample_df.columns if ("avg_3" in col or "avg_5" in col) and not col.startswith("opp_")]

# Process each enriched team file
for file in glob(os.path.join(input_dir, "*_enriched.csv")):
    team_abbr = os.path.basename(file).split("_")[0]
    df = pd.read_csv(file)

    # Parse GAME_DATE
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

    # Prepare output columns
    for stat in rolling_cols:
        df[f"opp_{stat}"] = None

    for idx, row in df.iterrows():
        opp = row["opponent_abbr"]
        game_date = row["GAME_DATE"]

        try:
            opp_file = os.path.join(opponent_dir, f"{opp}_rolling_flags_opp.csv")
            opp_df = pd.read_csv(opp_file)
            opp_df["GAME_DATE"] = pd.to_datetime(opp_df["GAME_DATE"])

            # Get most recent game BEFORE this matchup
            opp_prior = opp_df[opp_df["GAME_DATE"] < game_date]
            if opp_prior.empty:
                continue

            latest_row = opp_prior.iloc[-1]
            for stat in rolling_cols:
                df.at[idx, f"opp_{stat}"] = latest_row.get(stat, None)

        except Exception as e:
            print(f"⚠️ Failed for {team_abbr} vs {opp}: {e}")

    # Save result
    output_path = os.path.join(output_dir, f"{team_abbr}_enriched_opp_rolling.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Done: {team_abbr}")
