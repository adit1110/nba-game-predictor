import pandas as pd
import joblib
from itertools import permutations
import os

# Load model
model = joblib.load("../models/logreg_model.pkl")

# Load team averages from gamelogs
team_df = pd.read_csv("../data/raw/team_averages_from_gamelogs.csv")
team_df.columns = [col.replace("FG_PCT", "FG%").replace("REB", "TRB") for col in team_df.columns]

# Build team stats dictionary
team_stats = {}
for _, row in team_df.iterrows():
    team = row["Team"]
    team_stats[team] = {
        "AST": float(row["AST"]),
        "TRB": float(row["TRB"]),
        "FG%": float(row["FG%"]),
        "TOV": float(row["TOV"])
    }

# Simulate matchups
teams = list(team_stats.keys())
results = {team: 0 for team in teams}

for home, away in permutations(teams, 2):
    if home == away:
        continue

    # Prepare input features
    input_data = {
        "Home_AST": team_stats[home]["AST"],
        "Away_AST": team_stats[away]["AST"],
        "Home_TRB": team_stats[home]["TRB"],
        "Away_TRB": team_stats[away]["TRB"],
        "Home_FG%": team_stats[home]["FG%"],
        "Away_FG%": team_stats[away]["FG%"],
        "Home_TOV": team_stats[home]["TOV"],
        "Away_TOV": team_stats[away]["TOV"],
    }

    df = pd.DataFrame([input_data])
    if df.isnull().any().any():
        print(f"⚠️ Skipping {home} vs {away} due to missing data.")
        continue

    pred = model.predict(df)[0]

    if pred == 1:
        results[home] += 1
    else:
        results[away] += 1

# Final standings
standings = pd.DataFrame(list(results.items()), columns=["Team", "Wins"])
standings = standings.sort_values(by="Wins", ascending=False).reset_index(drop=True)

print("🏆 Simulated Season Standings:")
print(standings)
