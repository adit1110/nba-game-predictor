import { useState } from 'react';

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
  

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert("Please select two different teams.");
      return;
    }

    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam })
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-blue-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md text-center">
        <h1 className="text-3xl font-bold text-orange-600 mb-6 flex justify-center items-center gap-2">
          🏀 <span>NBA Matchup Predictor</span>
        </h1>

        <div className="flex flex-col gap-6 mb-6">
  {/* Home Team Logo */}
  {homeTeam && (
    <div className="flex flex-col items-center">
      <img
        src={`https://cdn.nba.com/logos/nba/${teamIdMap[homeTeam]}/global/L/logo.svg`}
        alt={`${homeTeam} logo`}
        className="max-h-10 max-w-[48px] w-full object-contain"
      />
      <p className="text-sm text-gray-600 mt-1">{homeTeam}</p>
    </div>
  )}

  {/* Home Select */}
  <select
    className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
    value={homeTeam}
    onChange={(e) => setHomeTeam(e.target.value)}
  >
    <option value="">Select Home Team</option>
    {nbaTeams.map((team) => (
      <option key={team} value={team}>{team}</option>
    ))}
  </select>

  {/* VS Divider */}
  <p className="text-xl font-semibold text-gray-500">VS</p>

  {/* Away Team Logo */}
  {awayTeam && (
    <div className="flex flex-col items-center">
      <img
        src={`https://cdn.nba.com/logos/nba/${teamIdMap[awayTeam]}/global/L/logo.svg`}
        alt={`${awayTeam} logo`}
        className="max-h-10 max-w-[48px] w-full object-contain"
      />
      <p className="text-sm text-gray-600 mt-1">{awayTeam}</p>
    </div>
  )}

  {/* Away Select */}
  <select
    className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
    value={awayTeam}
    onChange={(e) => setAwayTeam(e.target.value)}
  >
    <option value="">Select Away Team</option>
    {nbaTeams.map((team) => (
      <option key={team} value={team}>{team}</option>
    ))}
  </select>

  {/* Predict Button */}
  <button
    className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition-all"
    onClick={handlePredict}
  >
    Predict
  </button>
</div>



        {result && (
          <div className="bg-blue-50 p-4 rounded shadow text-blue-800 font-medium">
            <h2 className="text-xl mb-2">Prediction Result</h2>
            <p className="text-lg">{result.winner}</p>
            <p className="text-sm text-gray-700 mt-1">Confidence: {result.confidence}%</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
