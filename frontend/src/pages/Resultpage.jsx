import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import StatComparisonChart from '../components/StatComparisonChart';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Select from 'react-select';
import { motion } from 'framer-motion';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

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

const nbaTeams = Object.keys(teamNameMap);

const teamOptions = Object.entries(teamNameMap).map(([abbr, name]) => ({
  value: abbr,
  label: `${name} (${abbr})`
}));


function ResultPage() {
  const query = useQuery();
  const navigate = useNavigate();

  const [homeTeam, setHomeTeam] = useState(query.get('home'));
  const [awayTeam, setAwayTeam] = useState(query.get('away'));
  const [result, setResult] = useState(null);

  const fetchPrediction = async () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) return;
    const res = await fetch('https://nba-game-predictor-trh9.onrender.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam })
    });
    const data = await res.json();
    setResult(data);
  };

  useEffect(() => {
    fetchPrediction();
  }, [homeTeam, awayTeam]);

  const handleRecalculate = () => {
    fetchPrediction();
  };

  return (
    <div className="flex flex-col min-h-screen font-[Arial]">
      <Header />
      <main className="flex-1 container mx-auto p-6">
        <div className="text-center mb-6">
          <h2 className="text-3xl text-blue-700 mb-4">Prediction Result</h2>

          <div className="flex justify-center gap-4 mb-4 flex-wrap">
          <Select
            options={teamOptions.filter(option => option.value !== awayTeam)}
            onChange={(option) => setHomeTeam(option.value)}
            value={teamOptions.find(opt => opt.value === homeTeam)}
            placeholder="Home Team"
            theme={(theme) => ({
                ...theme,
                borderRadius: 6,
                colors: {
                  ...theme.colors,
                  primary25: '#dbeafe',  // hover
                  primary: '#1d4ed8',    // selected
                },
              })}
              styles={{
  control: (base) => ({
    ...base,
    backgroundColor: 'white',
    borderColor: '#1d4ed8',
    fontWeight: '600',
    textTransform: 'uppercase',
    fontFamily: 'Anton, sans-serif',
    boxShadow: 'none',
    '&:hover': { borderColor: '#1e40af' }
  }),
  singleValue: (base) => ({
    ...base,
    color: '#1e3a8a',
  }),
  menu: (base) => ({
    ...base,
    backgroundColor: document.body.classList.contains('dark') ? '#1e293b' : 'white',
    color: document.body.classList.contains('dark') ? '#f8fafc' : 'black',
  }),
  option: (base, { isFocused }) => ({
    ...base,
    backgroundColor: isFocused
      ? (document.body.classList.contains('dark') ? '#334155' : '#dbeafe')
      : 'transparent',
    color: document.body.classList.contains('dark') ? '#f8fafc' : 'black',
  }),
}}

              className='w-48'              
            />

          <Select
            options={teamOptions.filter(option => option.value !== homeTeam)}
            onChange={(option) => setAwayTeam(option.value)}
            value={teamOptions.find(opt => opt.value === awayTeam)}
            placeholder="Away Team"
            theme={(theme) => ({
                ...theme,
                borderRadius: 6,
                colors: {
                  ...theme.colors,
                  primary25: '#dbeafe',  // hover
                  primary: '#1d4ed8',    // selected
                },
              })}
              styles={{
  control: (base) => ({
    ...base,
    backgroundColor: 'white',
    borderColor: '#1d4ed8',
    fontWeight: '600',
    textTransform: 'uppercase',
    fontFamily: 'Anton, sans-serif',
    boxShadow: 'none',
    '&:hover': { borderColor: '#1e40af' }
  }),
  singleValue: (base) => ({
    ...base,
    color: '#1e3a8a',
  }),
  menu: (base) => ({
    ...base,
    backgroundColor: document.body.classList.contains('dark') ? '#1e293b' : 'white',
    color: document.body.classList.contains('dark') ? '#f8fafc' : 'black',
  }),
  option: (base, { isFocused }) => ({
    ...base,
    backgroundColor: isFocused
      ? (document.body.classList.contains('dark') ? '#334155' : '#dbeafe')
      : 'transparent',
    color: document.body.classList.contains('dark') ? '#f8fafc' : 'black',
  }),
}}

              className='w-48'              
            />

            <button onClick={handleRecalculate} className="bg-blue-700 text-white px-6 py-2 rounded hover:bg-blue-800">
              Recalculate
            </button>
          </div>

          {result?.winner && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className='flex flex-col items-center gap-3 mt-6'
            >
              <h3 className='text-2xl font-bold text-green-700'>🏆 Predicted Winner</h3>
              <div className="flex items-center gap-3">
                <img
                  src={`https://cdn.nba.com/logos/nba/${teamIdMap[result.winner === 'Home Wins' ? homeTeam : awayTeam]}/global/L/logo.svg`}
                  alt="Winner Logo"
                  className="w-16 h-16 object-contain"
                />
                <span className='text-xl font-semibold'>
                  {result.winner === 'Home Wins' ? teamNameMap[homeTeam] : teamNameMap[awayTeam]}
              </span>
            </div>
            <p className="text-sm text-gray-600">Confidence: {result.confidence}%</p>
          </motion.div>
          )}
        </div>


        {result?.home_stats && result?.away_stats && (
          <div className="flex flex-wrap justify-center gap-6">
            <div className="w-full md:w-1/2">
              <StatComparisonChart
                homeStats={result.home_stats}
                awayStats={result.away_stats}
                homeTeam={homeTeam}
                awayTeam={awayTeam}
              />
            </div>
            <div className="w-full md:w-1/3 flex items-center justify-center gap-4">
              <div className="w-16 h-16">
                <img src={`https://cdn.nba.com/logos/nba/${teamIdMap[homeTeam]}/global/L/logo.svg`} alt="Home Logo" className="w-full h-full object-contain" />
              </div>
              <span className="text-xl">VS</span>
              <div className="w-16 h-16">
                <img src={`https://cdn.nba.com/logos/nba/${teamIdMap[awayTeam]}/global/L/logo.svg`} alt="Away Logo" className="w-full h-full object-contain" />
              </div>
            </div>
          </div>
        )}

        <div className="text-center mt-8">
          <button
            onClick={() => navigate('/')}
            className="bg-blue-700 text-white px-4 py-2 rounded hover:bg-blue-800 transition"
          >
            ← Back to Homepage
          </button>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default ResultPage;