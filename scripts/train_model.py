import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# Load dataset
df = pd.read_csv("data/processed/final_training_data.csv")
df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

# Label: 1 if home team won
df["Home_Win"] = ((df["WL"] == "W") & (df["is_home"] == 1)) | ((df["WL"] == "L") & (df["is_home"] == 0))
df["Home_Win"] = df["Home_Win"].astype(int)

# Final feature set
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

# Ensure numeric, drop bad rows
df[features] = df[features].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=features + ["Home_Win"])

# Split & scale
X = df[features]
y = df["Home_Win"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest + Calibrator
rf = RandomForestClassifier(n_estimators=100, random_state=42)
calibrated_model = CalibratedClassifierCV(rf, cv=5, method="sigmoid")
calibrated_model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = calibrated_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("Confusion Matrix:\n", conf_matrix)

# Save model and scaler
os.makedirs("../models", exist_ok=True)
joblib.dump(calibrated_model, "../models/logreg_model.pkl")
joblib.dump(scaler, "../models/scaler.pkl")
print("✅ Calibrated model + scaler saved to /models/")
