import { useState } from 'react';
import StatComparisonChart from './components/StatComparisonChart';

function App() {
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [result, setResult] = useState(null);

  const nbaTeams = [
    "ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET",
    "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
    "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
  ];

  const teamIdMap = {
    ATL: "1610612737", BKN: "1610612751", BOS: "1610612738", CHA: "1610612766",
    CHI: "1610612741", CLE: "1610612739", DAL: "1610612742", DEN: "1610612743",
    DET: "1610612765", GSW: "1610612744", HOU: "1610612745", IND: "1610612754",
    LAC: "1610612746", LAL: "1610612747", MEM: "1610612763", MIA: "1610612748",
    MIL: "1610612749", MIN: "1610612750", NOP: "1610612740", NYK: "1610612752",
    OKC: "1610612760", ORL: "1610612753", PHI: "1610612755", PHX: "1610612756",
    POR: "1610612757", SAC: "1610612758", SAS: "1610612759", TOR: "1610612761",
    UTA: "1610612762", WAS: "1610612764"
  };
  

  const teamNameMap = {
    ATL: "Atlanta Hawks", BKN: "Brooklyn Nets", BOS: "Boston Celtics", CHA: "Charlotte Hornets",
    CHI: "Chicago Bulls", CLE: "Cleveland Cavaliers", DAL: "Dallas Mavericks", DEN: "Denver Nuggets",
    DET: "Detroit Pistons", GSW: "Golden State Warriors", HOU: "Houston Rockets", IND: "Indiana Pacers",
    LAC: "LA Clippers", LAL: "Los Angeles Lakers", MEM: "Memphis Grizzlies", MIA: "Miami Heat",
    MIL: "Milwaukee Bucks", MIN: "Minnesota Timberwolves", NOP: "New Orleans Pelicans", NYK: "New York Knicks",
    OKC: "Oklahoma City Thunder", ORL: "Orlando Magic", PHI: "Philadelphia 76ers", PHX: "Phoenix Suns",
    POR: "Portland Trail Blazers", SAC: "Sacramento Kings", SAS: "San Antonio Spurs", TOR: "Toronto Raptors",
    UTA: "Utah Jazz", WAS: "Washington Wizards"
  };
  
  
  const handlePredict = async () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert("Please select two different teams.");
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Prediction error:", error);
      alert("Error making prediction. See console for details.");
    }
  };
  
  return (
    <div className="font-sans min-h-screen bg-gradient-to-br from-white via-blue-50 to-blue-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md text-center">

        {/* Logos Above Title */}
        {homeTeam && awayTeam && (
          <div className="flex items-center justify-center gap-4 mb-4">
            <div className="w-16 h-16 flex justify-center items-center">
              <img
                src={`https://cdn.nba.com/logos/nba/${teamIdMap[homeTeam]}/global/L/logo.svg`}
                alt={`${homeTeam} logo`}
                className="w-full h-full object-contain"
              />
            </div>
            <span className="font-title text-gray-500 text-3xl">VS</span>
            <div className="w-16 h-16 flex justify-center items-center">
              <img
                src={`https://cdn.nba.com/logos/nba/${teamIdMap[awayTeam]}/global/L/logo.svg`}
                alt={`${awayTeam} logo`}
                className="w-full h-full object-contain"
              />
            </div>
          </div>
        )}
        
        {/* Title */}
        <h1 className="text-5xl text-orange-600 mb-8 tracking-wider font-title">
          🏀 NBA Matchup Predictor
        </h1>

        {/* Home Team Select */}
        <select
          className="mt-2 px-4 py-2 w-44 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={homeTeam}
          onChange={(e) => setHomeTeam(e.target.value)}
        >
          <option value="">Home Team</option>
          {nbaTeams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>

        {/* VS Text */}
        <div className="text-center text-3xl my-6 font-title tracking-widest text-gray-600">
          VS
        </div>

        {/* Away Team Select */}
        <select
          className="mt-2 px-4 py-2 w-44 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={awayTeam}
          onChange={(e) => setAwayTeam(e.target.value)}
        >
          <option value="">Away Team</option>
          {nbaTeams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>

        {/* Add a spacer div */}
        <div className="h-16"></div>

        {/* Predict Button - Now completely separate with fixed height spacer above */}
        <button
          onClick={handlePredict}
          className="bg-white hover:bg-gray-100 text-black font-semibold py-3 px-6 rounded-md shadow-md border border-black"
        >
          Predict
        </button>

        {/* Result Display */}
        {result && (
          <div className="bg-blue-50 p-4 rounded shadow text-blue-800 font-medium mt-6">
            <h2 className="text-xl mb-2">
            🏆 {result.winner === "Home Wins" ? teamNameMap[homeTeam] : teamNameMap[awayTeam]} will win
            </h2>
            <p className="text-lg">{result.prediction}</p>
            <p className="text-sm text-gray-700 mt-1">
              Confidence: {result.confidence}%
            </p>
          </div>
        )}
        
        {result && result.home_stats && result.away_stats && (
          <StatComparisonChart
          homeStats={result.home_stats}
          awayStats={result.away_stats}
          homeTeam={homeTeam}
          awayTeam={awayTeam}
        />        
      )}
      </div>
    </div>
  );
}

export default App;