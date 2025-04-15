import pandas as pd
import numpy as np
import joblib
import os

# Load model + scaler
model = joblib.load("../models/logreg_model.pkl")
scaler = joblib.load("../models/scaler.pkl")

# Load full combined dataset
team_data = pd.read_csv("../data/processed/final_training_data_combined.csv")
team_data["GAME_DATE"] = pd.to_datetime(team_data["GAME_DATE"])

def get_latest_row(team_abbr):
    team_df = team_data[team_data["Team"] == team_abbr]
    if team_df.empty:
        raise ValueError(f"No data found for team {team_abbr}")
    return team_df.sort_values("GAME_DATE").iloc[-1]

def predict_matchup(home_team, away_team):
    try:
        home = get_latest_row(home_team)
        away = get_latest_row(away_team)
    except Exception as e:
        print("❌", e)
        return None

    features = {
        "PTS_avg_3": home["PTS_avg_3"],
        "PTS_avg_5": home["PTS_avg_5"],
        "AST_avg_3": home["AST_avg_3"],
        "AST_avg_5": home["AST_avg_5"],
        "TOV_avg_3": home["TOV_avg_3"],
        "TOV_avg_5": home["TOV_avg_5"],
        "FG_PCT_avg_3": home["FG_PCT_avg_3"],
        "FG_PCT_avg_5": home["FG_PCT_avg_5"],
        "opp_PTS_avg_3": away["PTS_avg_3"],
        "opp_PTS_avg_5": away["PTS_avg_5"],
        "opp_AST_avg_3": away["AST_avg_3"],
        "opp_AST_avg_5": away["AST_avg_5"],
        "opp_TOV_avg_3": away["TOV_avg_3"],
        "opp_TOV_avg_5": away["TOV_avg_5"],
        "opp_FG_PCT_avg_3": away["FG_PCT_avg_3"],
        "opp_FG_PCT_avg_5": away["FG_PCT_avg_5"],
        "opp_AST_avg_season": away["opp_AST_avg_season"],
        "opp_TRB_avg_season": away["opp_TRB_avg_season"],
        "opp_FG%_avg_season": away["opp_FG%_avg_season"],
        "opp_TOV_avg_season": away["opp_TOV_avg_season"],
        "is_home": 1,
        "win_streak": home["win_streak"],
        "rest_days": home["rest_days"],
        "back_to_back": home["back_to_back"]
    }

    df = pd.DataFrame([features])
    X = scaler.transform(df)
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][pred]

    return {
        "prediction": "Home Wins" if pred == 1 else "Away Wins",
        "confidence": round(prob * 100, 2)
    }

if __name__ == "__main__":
    home = input("Enter Home Team Abbreviation (e.g. BKN): ").strip().upper()
    away = input("Enter Away Team Abbreviation (e.g. PHI): ").strip().upper()
    result = predict_matchup(home, away)
    if result:
        print(f"🏀 Prediction: {result['prediction']} ({result['confidence']}% confidence)")
