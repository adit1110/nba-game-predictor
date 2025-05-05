import os

folder = "../data/processed/enriched"

for filename in os.listdir(folder):
    if filename.endswith("_enriched_opp_rolling.csv"):
        old_path = os.path.join(folder, filename)
        new_filename = filename.replace("_enriched_opp_rolling.csv", "_enriched.csv")
        new_path = os.path.join(folder, new_filename)
        os.rename(old_path, new_path)
        print(f"✅ Renamed: {filename} → {new_filename}")
