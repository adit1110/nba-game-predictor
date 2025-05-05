# scripts/simulate_playoffs.py

from predict import predict_matchup

# Updated 2024–25 Conference Semifinals bracket
initial_matchups = {
    "West Semis": [("OKC", "DEN"), ("MIN", "GSW")],
    "East Semis": [("CLE", "IND"), ("NYK", "BOS")]
}

def simulate_round(matchups):
    results = []
    winners = []
    for home, away in matchups:
        prediction = predict_matchup(home, away)
        if not prediction:
            continue
        winner = home if prediction["winner"] == "Home Wins" else away
        results.append({
            "home": home,
            "away": away,
            "winner": winner,
            "confidence": prediction["confidence"]
        })
        winners.append(winner)
    return results, winners

def run_simulation():
    bracket = {"Rounds": {}}

    # Semis
    bracket["Rounds"]["West Semis"], west_winners = simulate_round(initial_matchups["West Semis"])
    bracket["Rounds"]["East Semis"], east_winners = simulate_round(initial_matchups["East Semis"])

    # Conference Finals
    bracket["Rounds"]["West Finals"], west_finalists = simulate_round([tuple(west_winners)])
    bracket["Rounds"]["East Finals"], east_finalists = simulate_round([tuple(east_winners)])

    # NBA Finals
    bracket["Rounds"]["NBA Finals"], final_winner = simulate_round([tuple([west_finalists[0], east_finalists[0]])])
    bracket["Champion"] = final_winner[0]

    return bracket

if __name__ == "__main__":
    import json
    result = run_simulation()
    print(json.dumps(result, indent=2))
