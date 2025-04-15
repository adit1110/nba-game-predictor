import os
import pandas as pd
from glob import glob

# Paths
input_dir = "../data/processed/contextualized"
output_path = "../data/processed/final_training_data.csv"

# Collect all final CSVs
all_files = glob(os.path.join(input_dir, "*_final.csv"))
all_data = []

for file in all_files:
    try:
        df = pd.read_csv(file)
        df["Team"] = os.path.basename(file).split("_")[0]  # tag with team
        all_data.append(df)
    except Exception as e:
        print(f"⚠️ Failed to read {file}: {e}")

# Combine all into one DataFrame
full_df = pd.concat(all_data, ignore_index=True)

# Drop rows with missing values (you can also use imputation later)
full_df_cleaned = full_df.dropna()

# Save to CSV
os.makedirs(os.path.dirname(output_path), exist_ok=True)
full_df_cleaned.to_csv(output_path, index=False)

print(f"✅ Final dataset saved to: {output_path}")
print(f"Total rows: {len(full_df_cleaned)}")
