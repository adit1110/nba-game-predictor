import subprocess

scripts = [           
    "add_opponent_season_stats.py",
    "add_opponent_column.py",
    "add_opponent_rolling_stats.py",
    "add_game_context_features.py",
    "build_final_training_data.py",
    "train_model.py"
]

print("🛠️ Starting full data pipeline...\n")

for script in scripts:
    print(f"➡️ Running {script}...")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("❌ Error:", result.stderr)

print("\n✅ Pipeline complete.")
