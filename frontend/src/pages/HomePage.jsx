import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Select from 'react-select';

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

const teamOptions = Object.entries(teamNameMap).map(([abbr, name]) => ({
  value: abbr,
  label: `${name} (${abbr})`
}));

function HomePage() {
  const navigate = useNavigate();
  const [homeTeam, setHomeTeam] = React.useState('');
  const [awayTeam, setAwayTeam] = React.useState('');

  const handleSubmit = () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert('Select two different teams.');
      return;
    }
    navigate(`/result?home=${homeTeam}&away=${awayTeam}`);
  };

  return (
    <div className="flex flex-col min-h-screen font-[Arial]">
      <Header />
      <main className="flex-1 flex items-center justify-center py-16 px-4">
        <div className="box shadow-xl rounded-lg p-8 w-full max-w-lg text-center">
          <h2 className="text-4xl text-blue-700 mb-6">Pick Two Teams</h2>

          <div className="flex flex-row gap-4 justify-center flex-wrap">
            <Select
              options={teamOptions.filter(option => option.value !== awayTeam)}
              onChange={(option) => setHomeTeam(option.value)}
              value={teamOptions.find(opt => opt.value === homeTeam)}
              placeholder="Home Team"
              className="w-48"
            />
            <Select
              options={teamOptions.filter(option => option.value !== homeTeam)}
              onChange={(option) => setAwayTeam(option.value)}
              value={teamOptions.find(opt => opt.value === awayTeam)}
              placeholder="Away Team"
              className="w-48"
            />
            <button
              onClick={handleSubmit}
              className="w-48 rounded shadow bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg shadow transition"
            >
              Predict
            </button>
            <button
              onClick={() => navigate('/playoffs')}
              className="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
            >
              Simulate Playoffs →
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default HomePage;
