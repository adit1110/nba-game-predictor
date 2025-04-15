from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# === Setup ===
app = Flask(__name__)
CORS(app)
model = joblib.load("logreg_model.pkl")
scaler = joblib.load("scaler.pkl")

CONFERENCES = {
    "East": {"ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DET", "IND", "MIA", "MIL", "NYK", "ORL", "PHI", "TOR", "WAS"},
    "West": {"DAL", "DEN", "GSW", "HOU", "LAC", "LAL", "MEM", "MIN", "NOP", "OKC", "PHX", "POR", "SAC", "SAS", "UTA"}
}

FEATURE_COLS = [
    "PTS_avg_3", "PTS_avg_5", "AST_avg_3", "AST_avg_5",
    "TOV_avg_3", "TOV_avg_5", "FG_PCT_avg_3", "FG_PCT_avg_5",
    "opp_PTS_avg_3", "opp_PTS_avg_5", "opp_AST_avg_3", "opp_AST_avg_5",
    "opp_TOV_avg_3", "opp_TOV_avg_5", "opp_FG_PCT_avg_3", "opp_FG_PCT_avg_5",
    "opp_AST_avg_season", "opp_TRB_avg_season", "opp_FG%_avg_season", "opp_TOV_avg_season",
    "is_home", "win_streak", "rest_days", "back_to_back"
]

stats_df = pd.read_csv("../data/processed/final_training_data.csv")
stats_df.columns = [col.replace("FG_PCT", "FG%") for col in stats_df.columns]
team_stats = {
    row["Team"]: {
        "PTS": float(row["PTS"]), "AST": float(row["AST"]),
        "TOV": float(row["TOV"]), "FG%": float(row["FG%"])
    } for _, row in stats_df.iterrows()
}

def build_features(home, away, is_home=1):
    return pd.DataFrame([{ 
        "PTS_avg_3": home["PTS"], "PTS_avg_5": home["PTS"],
        "AST_avg_3": home["AST"], "AST_avg_5": home["AST"],
        "TOV_avg_3": home["TOV"], "TOV_avg_5": home["TOV"],
        "FG_PCT_avg_3": home["FG%"], "FG_PCT_avg_5": home["FG%"],
        "opp_PTS_avg_3": away["PTS"], "opp_PTS_avg_5": away["PTS"],
        "opp_AST_avg_3": away["AST"], "opp_AST_avg_5": away["AST"],
        "opp_TOV_avg_3": away["TOV"], "opp_TOV_avg_5": away["TOV"],
        "opp_FG_PCT_avg_3": away["FG%"], "opp_FG_PCT_avg_5": away["FG%"],
        "opp_AST_avg_season": away["AST"], "opp_TRB_avg_season": 45.0,
        "opp_FG%_avg_season": away["FG%"], "opp_TOV_avg_season": away["TOV"],
        "is_home": is_home, "win_streak": 2, "rest_days": 1, "back_to_back": 0
    }])[FEATURE_COLS]

# === Routes ===
@app.route("/")
def home():
    return "NBA Predictor API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    home, away = data.get("home_team"), data.get("away_team")
    if not home or not away or home not in team_stats or away not in team_stats:
        return jsonify({"error": "Invalid team abbreviation(s)"}), 400

    df = build_features(team_stats[home], team_stats[away])
    pred = model.predict(scaler.transform(df))[0]
    prob = model.predict_proba(scaler.transform(df))[0][1 if pred == 1 else 0]

    return jsonify({"prediction": "Home Wins" if pred == 1 else "Away Wins", "confidence": round(prob * 100, 2)})

@app.route("/simulate-season", methods=["GET"])
def simulate_season():
    conference = request.args.get('conference')
    teams = list(CONFERENCES[conference]) if conference in CONFERENCES else list(team_stats.keys())
    results = {team: {"wins": 0, "losses": 0} for team in teams}

    for home_team in teams:
        for away_team in teams:
            if home_team == away_team: continue
            df = build_features(team_stats[home_team], team_stats[away_team])
            pred = model.predict(scaler.transform(df))[0]
            if pred == 1:
                results[home_team]["wins"] += 1
                results[away_team]["losses"] += 1
            else:
                results[away_team]["wins"] += 1
                results[home_team]["losses"] += 1

    return jsonify(dict(sorted(results.items(), key=lambda x: -x[1]["wins"])))

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conference = request.args.get('conference')
    teams = list(CONFERENCES[conference]) if conference in CONFERENCES else list(team_stats.keys())
    board = []
    for team in teams:
        wins = sum(
            model.predict(scaler.transform(build_features(team_stats[team], team_stats[opp])))[0] == 1
            for opp in teams if team != opp
        )
        losses = len(teams) - 1 - wins
        board.append({"team": team, "wins": wins, "losses": losses, "win_percentage": round(wins / (wins + losses), 3)})

    return jsonify(sorted(board, key=lambda x: -x["win_percentage"]))

@app.route("/playoffs", methods=["GET"])
def playoffs():
    def get_top_8(conf):
        return sorted(CONFERENCES[conf], key=lambda t: sum(
            model.predict(scaler.transform(build_features(team_stats[t], team_stats[o])))[0] == 1
            for o in CONFERENCES[conf] if t != o), reverse=True)[:8]

    def play_round(teams):
        return [
            h if model.predict(scaler.transform(build_features(team_stats[h], team_stats[a])))[0] == 1 else a
            for h, a in zip(teams[:4], reversed(teams[:4]))
        ]

    east = get_top_8("East")
    west = get_top_8("West")
    east_final = play_round(play_round(east))[0]
    west_final = play_round(play_round(west))[0]
    champ_df = build_features(team_stats[east_final], team_stats[west_final])
    champ = east_final if model.predict(scaler.transform(champ_df))[0] == 1 else west_final

    return jsonify({"Eastern Champ": east_final, "Western Champ": west_final, "NBA Champion": champ})

@app.route("/team/<abbr>", methods=["GET"])
def team_view(abbr):
    abbr = abbr.upper()
    if abbr not in team_stats:
        return jsonify({"error": "Invalid team abbreviation"}), 400

    matchups = []
    for opp in team_stats:
        if abbr == opp: continue
        df = build_features(team_stats[abbr], team_stats[opp])
        pred = model.predict(scaler.transform(df))[0]
        prob = model.predict_proba(scaler.transform(df))[0][1 if pred == 1 else 0]
        matchups.append({"opponent": opp, "result": "Win" if pred == 1 else "Loss", "confidence": round(prob * 100, 2)})

    return jsonify({"team": abbr, "matchups": sorted(matchups, key=lambda x: -x["confidence"])})

if __name__ == "__main__":
    app.run(debug=True)