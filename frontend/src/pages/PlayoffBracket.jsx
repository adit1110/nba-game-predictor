import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import BracketGrid from "../components/BracketGrid";

// NBA team ID map for logos
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

const roundNames = {
  "West Semis": "Western Conference Semifinals",
  "East Semis": "Eastern Conference Semifinals",
  "West Finals": "Western Conference Finals",
  "East Finals": "Eastern Conference Finals",
  "NBA Finals": "NBA Finals"
};

export default function PlayoffBracket() {
  const navigate = useNavigate();
  const [bracket, setBracket] = useState(null);
  const [loading, setLoading] = useState(true);

const toggleDarkMode = () => {
  document.body.classList.toggle('dark');
};


  useEffect(() => {
    fetch("http://localhost:5000/simulate_playoffs")
      .then((res) => res.json())
      .then((data) => {
        setBracket(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch bracket:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center text-xl mt-10">Loading Playoff Simulation...</div>;

  // Helper to render game card
  const GameCard = ({ home, away, winner, confidence, index }) => (
    <motion.div
      key={`${home}-${away}-${index}`}
      className="bg-white p-4 rounded-xl shadow-md hover:shadow-xl flex flex-col items-center text-center"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
    >
      <div className="flex items-center justify-center gap-3 mb-2">
        <TeamLogo abbr={away} />
        <span className="text-lg font-bold text-gray-700">@</span>
        <TeamLogo abbr={home} />
      </div>
      <p className="text-base">
        🏆 <span className="font-semibold text-green-600">{winner}</span> wins
      </p>
      <p className="text-sm text-gray-500">Confidence: {confidence.toFixed(2)}%</p>
    </motion.div>
  );

  const TeamLogo = ({ abbr }) => (
    <img
      src={`https://cdn.nba.com/logos/nba/${teamIdMap[abbr]}/global/L/logo.svg`}
      alt={abbr}
      className="w-10 h-10 object-contain"
    />
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-blue-100 px-4 py-8 font-[Arial]">
      <h1 className="text-4xl font-extrabold text-center text-blue-800 mb-12">🏀 2025 NBA Playoff Simulation</h1>
  
      {/* Desktop visual bracket */}
      <div>
        <BracketGrid data={bracket} />
      </div>
  
      {/* Mobile/tablet fallback layout */}
      <div className="block md:hidden">
        <div className="flex flex-wrap justify-evenly gap-8">
          {/* EAST */}
          <div className="w-full space-y-6">
            {["East Semis", "East Finals"].map((roundKey) => (
              <div key={roundKey}>
                <h2 className="text-xl font-bold text-center text-indigo-700 border-b pb-1 mb-3">{roundNames[roundKey]}</h2>
                <div className="grid grid-cols-1 gap-4">
                  {bracket.Rounds[roundKey]?.map((game, i) => (
                    <GameCard {...game} index={i} key={i} />
                  ))}
                </div>
              </div>
            ))}
          </div>
  
          {/* WEST */}
          <div className="w-full space-y-6">
            {["West Semis", "West Finals"].map((roundKey) => (
              <div key={roundKey}>
                <h2 className="text-xl font-bold text-center text-indigo-700 border-b pb-1 mb-3">{roundNames[roundKey]}</h2>
                <div className="grid grid-cols-1 gap-4">
                  {bracket.Rounds[roundKey]?.map((game, i) => (
                    <GameCard {...game} index={i} key={i} />
                  ))}
                </div>
              </div>
            ))}
          </div>
  
          {/* NBA Finals */}
          <div className="w-full mt-10">
            <h2 className="text-2xl font-bold text-center text-purple-800 mb-4 border-b pb-2">NBA Finals</h2>
            <div className="flex justify-center">
              {bracket.Rounds["NBA Finals"]?.map((game, i) => (
                <GameCard {...game} index={i} key={i} />
              ))}
            </div>
          </div>
        </div>
      </div>
  
      {/* Champion */}
      <div className="text-center mt-12">
        <h2 className="text-3xl font-bold text-green-700">🏆 NBA Champion: {bracket.Champion}</h2>
        <p className="text-sm text-gray-600 mt-2">Based on full playoff simulation</p>
  
        <button
          onClick={() => navigate("/")}
          className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg shadow transition"
        >
          ← Back to Homepage
        </button>
        <div className="mt-4 flex justify-center gap-4 flex-wrap">
        <button
          onClick={() => navigate("/result")}
          className="bg-blue-700 hover:bg-blue-800 text-white dark:text-white px-4 py-2 rounded transition"
        >
        Results
        </button>
        <button
          onClick={() => navigate("/playoffs")}
          className="bg-blue-700 hover:bg-blue-800 text-white dark:text-white px-4 py-2 rounded transition"
        >
        Playoffs
        </button>
        <button
        onClick={toggleDarkMode}
        className="bg-yellow-400 hover:bg-yellow-500 text-black dark:text-white px-4 py-2 rounded transition"
        >
          🌙 Toggle Dark Mode
        </button>
      </div>
      </div>
    </div>
  );  
}
