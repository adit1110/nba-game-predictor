# NBA Game Predictor

A sophisticated machine learning web application that predicts NBA game outcomes using advanced feature engineering, historical team performance data, and player-level analytics. Built with a modern full-stack architecture and achieving **~91.88% prediction accuracy**.

## Key Features

### Prediction Capabilities
- **Game Outcome Prediction**: Predict winner between any two NBA teams with confidence scores
- **Season Simulation**: Full season simulation with conference filtering
- **Playoff Bracket Simulation**: Complete playoff tournament predictions
- **Team Analytics**: Individual team performance analysis and matchup breakdowns

### Advanced ML Features
- **Multi-layered Feature Engineering**: Rolling averages (3/5-game windows), opponent stats, contextual features
- **Player-Level Analytics**: Top-3 player performance metrics and injury impact modeling
- **Calibrated Predictions**: Probability calibration for reliable confidence scores
- **Real-time Data Integration**: Live game fetching and prediction pipeline

### Full-Stack Architecture
- **Backend**: Flask REST API with comprehensive endpoints
- **Frontend**: React + Vite with interactive stat comparison charts
- **Models**: Calibrated Random Forest with StandardScaler preprocessing
- **Data Pipeline**: Automated ETL process with NBA API integration

## Project Architecture

```
NBA-Predictor/
├── backend/                    # Flask API server
│   ├── app.py                 # Main API with 8+ endpoints
│   ├── logreg_model.pkl       # Trained Random Forest model
│   └── scaler.pkl             # Feature scaling pipeline
├── frontend/                   # React + Vite application
├── models/                     # Saved ML models and scalers
├── data/
│   ├── raw/                   # Original NBA API data
│   │   ├── team_game_logs/    # Team performance data
│   │   └── player_game_logs/  # Individual player statistics
│   └── processed/             # Feature-engineered datasets
├── scripts/                    # Data processing & ML pipeline
│   ├── fetch_game_logs.py     # NBA API data collection
│   ├── train_model.py         # ML model training
│   ├── predict.py             # Standalone prediction engine
│   └── retrain_pipeline.py    # Automated retraining workflow
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- NBA API access

### 1. Clone & Setup
```bash
git clone https://github.com/adit1110/NBA-Predictor.git
cd NBA-Predictor
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*API will be available at `http://localhost:5000`*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Web app will be available at `http://localhost:5173`*

### 4. Data Pipeline (Optional)
```bash
cd scripts
python retrain_pipeline.py  # Full model retraining
python get_tonights_games.py  # Live game predictions
```

## API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/predict` | POST | Single game prediction with team stats |
| `/simulate-season` | GET | Full season simulation by conference |
| `/leaderboard` | GET | Team rankings with win percentages |
| `/playoffs` | GET | Complete playoff bracket simulation |
| `/team/<abbr>` | GET | Individual team analysis |
| `/simulate_playoffs` | GET | Advanced playoff simulation |

### Example API Usage
```javascript
// Predict Lakers vs Warriors
POST /predict
{
  "home_team": "LAL",
  "away_team": "GSW"
}

// Response
{
  "winner": "Home Wins",
  "confidence": 67.42,
  "home_stats": { "PTS": 118.4, "AST": 27.1, "FG%": 0.478 },
  "away_stats": { "PTS": 115.8, "AST": 28.3, "FG%": 0.465 }
}
```

## Model Details

### Feature Engineering Pipeline
- **Rolling Statistics**: 3/5-game rolling averages for PTS, AST, TOV, FG%
- **Opponent Analytics**: Historical opponent performance metrics
- **Contextual Features**: Win streaks, rest days, back-to-back games, home/away
- **Player Impact**: Top-3 player contributions and injury flags

### Model Architecture
- **Algorithm**: Calibrated Random Forest Classifier
- **Accuracy**: 91.88% on test set
- **Features**: 27 engineered features per prediction
- **Calibration**: Sigmoid probability calibration for confidence scores

### Training Features
```python
features = [
    # Team rolling averages
    "PTS_avg_3", "PTS_avg_5", "AST_avg_3", "AST_avg_5",
    "TOV_avg_3", "TOV_avg_5", "FG_PCT_avg_3", "FG_PCT_avg_5",
    
    # Opponent analytics
    "opp_PTS_avg_3", "opp_AST_avg_3", "opp_TOV_avg_3",
    "opp_AST_avg_season", "opp_TRB_avg_season",
    
    # Game context
    "is_home", "win_streak", "rest_days", "back_to_back",
    
    # Player-level features
    "top3_avg_pts", "top3_avg_ast", "missing_top_player"
]
```

## Data Sources & Processing

### NBA API Integration
- **Team Game Logs**: Complete 2023-24 season data via `nba_api`
- **Player Statistics**: Individual player performance metrics
- **Live Games**: Real-time game scheduling and results

### Data Processing Pipeline
1. **Raw Data Collection**: Automated NBA API scraping with rate limiting
2. **Feature Engineering**: Multi-stage processing with rolling averages
3. **Opponent Integration**: Cross-referencing opponent historical performance
4. **Context Addition**: Game situation features (rest, streaks, venue)
5. **Player Analytics**: Top performer identification and injury modeling

## Advanced Features

### Automated Retraining
```bash
python scripts/retrain_pipeline.py
```
- Fetches latest NBA data
- Rebuilds feature engineering pipeline
- Retrains model with updated data
- Validates performance metrics

### Live Game Integration
```bash
python scripts/get_tonights_games.py
```
- Fetches today's NBA schedule
- Generates predictions for all games
- Outputs formatted predictions with confidence

### Playoff Simulation
- Simulates complete playoff brackets
- Conference championship predictions
- NBA Finals outcome prediction
- Accounts for playoff momentum and matchup advantages

## Frontend Features

- **Interactive Predictions**: Real-time team selection and prediction
- **Statistical Comparisons**: Side-by-side team stat visualizations
- **Season Simulation**: Conference standings and playoff projections
- **Responsive Design**: Mobile-optimized interface
- **Live Updates**: Real-time prediction updates

## Performance Metrics

- **Accuracy**: 91.88% on held-out test set
- **Precision**: High precision for both home/away predictions
- **Calibration**: Well-calibrated probability estimates
- **Speed**: Sub-100ms prediction response times
- **Scalability**: Handles 30+ team concurrent predictions

## Roadmap

### Immediate Improvements
- [ ] Real-time injury data integration
- [ ] Advanced player efficiency metrics
- [ ] Betting line integration and comparison
- [ ] Historical prediction tracking

### Future Enhancements
- [ ] Deep learning model exploration (LSTM for sequence modeling)
- [ ] Real-time model updating during games
- [ ] Multi-season trend analysis
- [ ] Advanced visualization dashboard
- [ ] Mobile app development


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **NBA API**: Official NBA statistics and data
- **Basketball Reference**: Historical NBA data validation
- **FastF1 Project**: Inspiration for sports prediction architecture
- **scikit-learn**: Machine learning framework and tools

## Author

**Adit Bhimani**
- GitHub: [@adit1110](https://github.com/adit1110)
- Project Link: [NBA-Predictor](https://github.com/adit1110/NBA-Predictor)
