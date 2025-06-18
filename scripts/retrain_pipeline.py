# retrain_pipeline.py
import subprocess

steps = [
    ("Fetching team game logs", "python fetch_game_logs.py"),
    ("Generating rolling averages", "python generate_rolling_averages.py"),
    ("Building final training data", "python build_final_training_data.py"),
    ("Fetching player game logs", "python fetch_player_game_logs.py"),
    ("Adding player-level features", "python add_player_level_features.py"),
    ("Retraining model with player data", "python train_model.py --use_player_data")
]

print("\n🚀 Starting full model retraining pipeline...\n")

for label, command in steps:
    print(f"🔄 {label}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {label} complete\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ {label} failed: {e}\n")
        break

print("🎉 Pipeline finished!")
