import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const nbaTeams = [
  "ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET",
  "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
  "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
];

function HomePage() {
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert('Select two different teams.');
      return;
    }
    navigate(`/result?home=${homeTeam}&away=${awayTeam}`);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-1 flex items-center justify-center py-16 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8 w-full max-w-lg text-center">
          <h2 className="text-4xl text-blue-700 font-bold mb-6">Pick Two Teams</h2>
          <select value={homeTeam} onChange={(e) => setHomeTeam(e.target.value)} className="w-64 mb-4 px-4 py-2 border rounded-md">
            <option value="">Home Team</option>
            {nbaTeams.map(team => <option key={team} value={team}>{team}</option>)}
          </select>
          <select value={awayTeam} onChange={(e) => setAwayTeam(e.target.value)} className="w-64 mb-6 px-4 py-2 border rounded-md">
            <option value="">Away Team</option>
            {nbaTeams.map(team => <option key={team} value={team}>{team}</option>)}
          </select>
          <button onClick={handleSubmit} className="bg-blue-700 text-white px-6 py-2 rounded hover:bg-blue-800">Predict</button>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default HomePage;
