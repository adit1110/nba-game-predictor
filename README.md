# NBA Game Predictor

An end-to-end machine learning web app that predicts the outcome of NBA games based on historical team performance, engineered features like rolling averages and rest days, and a modern full-stack pipeline. Built with inspiration from the FastF1 project for Formula 1.

## Features

- Predict winner between any two NBA teams
- Confidence score for prediction
- Custom feature engineering (e.g., 3/5-game rolling averages, back-to-backs)
- REST API built with Flask
- React + Vite frontend with stat comparison charts
- Playoff simulation mode
- Team leaderboard and conference filtering

## Project Structure

NBA-Predictor/
├── backend/               # Flask API for predictions  
├── frontend/              # React frontend (Vite-powered)  
├── models/                # Saved ML models and scalers  
├── data/  
│   ├── raw/               # Original CSV exports  
│   └── processed/         # Cleaned and feature-engineered data  
├── scripts/  
│   ├── train_model.py     # Model training script  
│   └── predict.py         # Standalone prediction script  
└── README.md

## Getting Started

### 1. Clone the Repository

git clone https://github.com/yourusername/NBA-Predictor.git  
cd NBA-Predictor

### 2. Backend Setup (Flask API)

cd backend  
pip install -r requirements.txt  
python app.py

### 3. Frontend Setup (React + Vite)

cd ../frontend  
npm install  
npm run dev

Your app should now be live at http://localhost:5173

## Model Details

- Model: Random Forest Classifier (via scikit-learn)  
- Accuracy: ~91.88%  
- Features:  
  - Rolling averages for PTS, AST, TOV, FG%  
  - Opponent averages  
  - Win streak, rest days, back-to-back indicator  
  - Home vs. Away flag  

Models are saved to /models/logreg_model.pkl and scaler.pkl

## Data Sources

- Basketball Reference: https://www.basketball-reference.com/  
- CSV exports covering:  
  - Team totals  
  - Per-game stats  
  - Advanced metrics  
  - Shooting splits  

## Live Demo

Frontend Deployment: Vercel  
Backend Deployment: Render or local Flask instance

## Demo (Optional)

Include a Loom video walkthrough or GIFs of the UI in action.

## Credits

- Project inspired by the FastF1 F1 Predictor (https://github.com/theOehrly/Fast-F1)  
- Built by Adit Bhimani

## Future Improvements

- Add player-level stats  
- Improve visualizations (e.g., team logos, animated charts)  
- Scheduled model retraining  
- Full playoff and season simulations

## License

MIT License
