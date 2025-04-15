import os
import pandas as pd
from glob import glob

# Paths
current_dir = "../data/processed/contextualized"
multi_dir = "../data/processed_all_seasons/contextualized"
output_path = "../data/processed/final_training_data_combined.csv"

# Load current season data
current_files = glob(os.path.join(current_dir, "*_final.csv"))
multi_files = glob(os.path.join(multi_dir, "*_final.csv"))

all_data = []

for file in current_files + multi_files:
    try:
        df = pd.read_csv(file)
        df["Team"] = os.path.basename(file).split("_")[0]
        all_data.append(df)
    except Exception as e:
        print(f"⚠️ Failed to read {file}: {e}")

# Combine and clean
full_df = pd.concat(all_data, ignore_index=True)
full_df_cleaned = full_df.dropna()

# Save
os.makedirs(os.path.dirname(output_path), exist_ok=True)
full_df_cleaned.to_csv(output_path, index=False)

print(f"✅ Combined training data saved to: {output_path}")
print(f"Total rows: {len(full_df_cleaned)}")
