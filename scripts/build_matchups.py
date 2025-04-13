import os
import pandas as pd
from glob import glob

# Folder containing team gamelogs
LOG_DIR = os.path.join("..", "data", "raw", "team_game_logs")
SAVE_PATH = os.path.join("..", "data", "processed", "matchups.csv")

# Load all game logs into a dictionary
log_files = glob(os.path.join(LOG_DIR, "*.csv"))
team_logs = {}

for file in log_files:
    team_abbr = os.path.basename(file).split("_")[0]
    df = pd.read_csv(file)
    df['Team'] = team_abbr
    team_logs[team_abbr] = df

# Combine all logs into a single DataFrame for matching
all_games = pd.concat(team_logs.values(), ignore_index=True)

# Function to determine home and away teams
def get_home_away(row):
    if "vs." in row["MATCHUP"]:
        return row["Team"], row["MATCHUP"].split("vs.")[1].strip()
    else:
        return row["MATCHUP"].split("@")[1].strip(), row["Team"]

# Build the matchup rows
matchups = []

for _, row in all_games.iterrows():
    home, away = get_home_away(row)
    game_id = row["Game_ID"]
    date = row["GAME_DATE"]

    # Find the opponent's game entry
    opp_game = all_games[
        (all_games["Game_ID"] == game_id) & (all_games["Team"] == away)
    ]
    if opp_game.empty:
        continue  # Skip incomplete games

    opp_row = opp_game.iloc[0]

    # Get stats from both teams
    home_stats = row if row["Team"] == home else opp_row
    away_stats = row if row["Team"] == away else opp_row

    # Determine winner by comparing points
    home_pts = home_stats["PTS"]
    away_pts = away_stats["PTS"]

    if home_pts > away_pts:
        winner = home
    elif away_pts > home_pts:
        winner = away
    else:
        winner = "Draw"  # extremely rare in NBA

    # Build matchup dictionary
    matchups.append({
        "Date": date,
        "Home": home,
        "Away": away,
        "Home_PTS": home_pts,
        "Away_PTS": away_pts,
        "Winner": winner,
        "Home_FG_PCT": home_stats["FG_PCT"],
        "Away_FG_PCT": away_stats["FG_PCT"],
        "Home_REB": home_stats["REB"],
        "Away_REB": away_stats["REB"],
        "Home_AST": home_stats["AST"],
        "Away_AST": away_stats["AST"],
        "Home_TOV": home_stats["TOV"],
        "Away_TOV": away_stats["TOV"],
        "Home_STL": home_stats["STL"],
        "Away_STL": away_stats["STL"]
    })

# Save to CSV
matchup_df = pd.DataFrame(matchups)
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
matchup_df.to_csv(SAVE_PATH, index=False)

print(f"✅ Matchup dataset saved to: {SAVE_PATH}")
