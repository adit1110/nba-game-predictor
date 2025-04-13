import requests

TEAM_TRANSLATIONS = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA", "Washington Wizards": "WAS"
}

def fetch_games():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    response = requests.get(url)
    data = response.json()
    return data.get("events", [])

def predict_game(home_abbr, away_abbr):
    payload = {"home_team": home_abbr, "away_team": away_abbr}
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["prediction"], result["confidence"]
        else:
            return "Error", 0
    except requests.exceptions.ConnectionError:
        return "Server Not Running", 0

def main():
    games = fetch_games()
    if not games:
        print("No games found for today.")
        return

    print("🔮 Predictions for Tonight's NBA Games:\n")
    for game in games:
        comps = game["competitions"][0]["competitors"]
        home = next(c for c in comps if c["homeAway"] == "home")["team"]["displayName"]
        away = next(c for c in comps if c["homeAway"] == "away")["team"]["displayName"]

        home_abbr = TEAM_TRANSLATIONS.get(home)
        away_abbr = TEAM_TRANSLATIONS.get(away)

        if home_abbr and away_abbr:
            prediction, confidence = predict_game(home_abbr, away_abbr)
            print(f"🏀 {away_abbr} @ {home_abbr} → {prediction} ({confidence:.2f}%)")

if __name__ == "__main__":
    main()
