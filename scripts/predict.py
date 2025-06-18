import pandas as pd
import numpy as np
import joblib
import os

# Load model and scaler
model = joblib.load(os.path.join("..", "models", "logreg_model.pkl"))
scaler = joblib.load(os.path.join("..", "models", "scaler.pkl"))

# Load enhanced dataset with player-level features
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "final_training_data_with_players.csv"))
team_data = pd.read_csv(data_path)
team_data.set_index("Team", inplace=True)

def safe_get(series, key):
    val = series.get(key, 0)
    return val.item() if hasattr(val, "item") else val

def predict_matchup(home_team, away_team):
    try:
        home = team_data.loc[home_team].sort_values("GAME_DATE").iloc[-1]
        away = team_data.loc[away_team].sort_values("GAME_DATE").iloc[-1]
    except KeyError as e:
        print(f"❌ Team abbreviation not found: {e}")
        return None

    features = {
        "PTS_avg_3": safe_get(home, "PTS_avg_3"),
        "PTS_avg_5": safe_get(home, "PTS_avg_5"),
        "AST_avg_3": safe_get(home, "AST_avg_3"),
        "AST_avg_5": safe_get(home, "AST_avg_5"),
        "TOV_avg_3": safe_get(home, "TOV_avg_3"),
        "TOV_avg_5": safe_get(home, "TOV_avg_5"),
        "FG_PCT_avg_3": safe_get(home, "FG_PCT_avg_3"),
        "FG_PCT_avg_5": safe_get(home, "FG_PCT_avg_5"),
        "opp_PTS_avg_3": safe_get(away, "PTS_avg_3"),
        "opp_PTS_avg_5": safe_get(away, "PTS_avg_5"),
        "opp_AST_avg_3": safe_get(away, "AST_avg_3"),
        "opp_AST_avg_5": safe_get(away, "AST_avg_5"),
        "opp_TOV_avg_3": safe_get(away, "TOV_avg_3"),
        "opp_TOV_avg_5": safe_get(away, "TOV_avg_5"),
        "opp_FG_PCT_avg_3": safe_get(away, "FG_PCT_avg_3"),
        "opp_FG_PCT_avg_5": safe_get(away, "FG_PCT_avg_5"),
        "opp_AST_avg_season": safe_get(away, "AST_avg_season"),
        "opp_TRB_avg_season": safe_get(away, "TRB_avg_season"),
        "opp_FG%_avg_season": safe_get(away, "FG%_avg_season"),
        "opp_TOV_avg_season": safe_get(away, "TOV_avg_season"),
        "is_home": 1,
        "win_streak": safe_get(home, "win_streak"),
        "rest_days": safe_get(home, "rest_days"),
        "back_to_back": safe_get(home, "back_to_back"),
        "top3_avg_pts": safe_get(home, "top3_avg_pts"),
        "top3_avg_ast": safe_get(home, "top3_avg_ast"),
        "missing_top_player": safe_get(home, "missing_top_player")
    }

    df = pd.DataFrame([features])
    X = scaler.transform(df)
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0][prediction] * 100

    result = {
        "winner": "Home Wins" if prediction == 1 else "Away Wins",
        "confidence": round(confidence, 2),
        "home_stats": {
            "PTS": safe_get(home, "PTS_avg_5"),
            "REB": safe_get(home, "REB"),
            "AST": safe_get(home, "AST_avg_5"),
            "FG%": safe_get(home, "FG_PCT_avg_5"),
            "Top3 PTS": safe_get(home, "top3_avg_pts"),
            "Top3 AST": safe_get(home, "top3_avg_ast"),
            "Injury Flag": bool(safe_get(home, "missing_top_player"))
        },
        "away_stats": {
            "PTS": safe_get(away, "PTS_avg_5"),
            "REB": safe_get(away, "REB"),
            "AST": safe_get(away, "AST_avg_5"),
            "FG%": safe_get(away, "FG_PCT_avg_5")
        }
    }
    return result

if __name__ == "__main__":
    home = input("Enter Home Team Abbreviation (e.g. BKN): ").strip().upper()
    away = input("Enter Away Team Abbreviation (e.g. PHI): ").strip().upper()
    result = predict_matchup(home, away)
    if result:
        print(f"\n🏀 Prediction: {result['winner']} ({result['confidence']}% confidence)")
