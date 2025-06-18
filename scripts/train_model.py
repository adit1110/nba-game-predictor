# train_model.py (Unified with Player-Level Support)
import pandas as pd
import os
import joblib
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# Argument parser to switch datasets
parser = argparse.ArgumentParser()
parser.add_argument("--use_player_data", action="store_true", help="Use player-level enhanced dataset")
args = parser.parse_args()

# Load appropriate dataset
if args.use_player_data:
    print("📥 Using enhanced dataset with player-level features...")
    df = pd.read_csv("../data/processed/final_training_data_with_players.csv")
else:
    print("📥 Using standard team-level dataset...")
    df = pd.read_csv("../data/processed/final_training_data.csv")

df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
df["Home_Win"] = ((df["WL"] == "W") & (df["is_home"] == 1)) | ((df["WL"] == "L") & (df["is_home"] == 0))
df["Home_Win"] = df["Home_Win"].astype(int)

# Base feature set
features = [
    "PTS_avg_3", "PTS_avg_5",
    "AST_avg_3", "AST_avg_5",
    "TOV_avg_3", "TOV_avg_5",
    "FG_PCT_avg_3", "FG_PCT_avg_5",
    "opp_PTS_avg_3", "opp_PTS_avg_5",
    "opp_AST_avg_3", "opp_AST_avg_5",
    "opp_TOV_avg_3", "opp_TOV_avg_5",
    "opp_FG_PCT_avg_3", "opp_FG_PCT_avg_5",
    "opp_AST_avg_season", "opp_TRB_avg_season",
    "opp_FG%_avg_season", "opp_TOV_avg_season",
    "is_home", "win_streak", "rest_days", "back_to_back"
]

# Add player-level features if needed
if args.use_player_data:
    features += ["top3_avg_pts", "top3_avg_ast", "missing_top_player"]

# Clean + split
df[features] = df[features].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=features + ["Home_Win"])

X = df[features]
y = df["Home_Win"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train calibrated random forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
calibrated_model = CalibratedClassifierCV(rf, cv=5, method="sigmoid")
calibrated_model.fit(X_train_scaled, y_train)

y_pred = calibrated_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
print("Confusion Matrix:\n", conf_matrix)

# Save model + scaler
os.makedirs("../models", exist_ok=True)
joblib.dump(calibrated_model, "../models/logreg_model.pkl")
joblib.dump(scaler, "../models/scaler.pkl")
print("\n✅ Calibrated model + scaler saved to /models/")
