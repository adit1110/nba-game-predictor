import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";



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

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-center mb-6">🏀 Simulated 2025 NBA Playoffs</h1>

      {Object.entries(bracket.Rounds).map(([roundKey, games]) => (
        <div key={roundKey} className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">{roundNames[roundKey]}</h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {games.map(({ home, away, winner, confidence }, index) => (
              <motion.div
                key={`${home}-${away}-${index}`}
                className="border rounded-2xl p-4 shadow-lg bg-white"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
              >
                <p className="text-lg">
                  <strong>{away}</strong> @ <strong>{home}</strong>
                </p>
                <p>
                  🏆 Predicted Winner: <span className="font-medium text-green-600">{winner}</span>
                </p>
                <p className="text-sm text-gray-500">Confidence: {confidence.toFixed(2)}%</p>
              </motion.div>
            ))}
          </div>
        </div>
      ))}

      <div className="text-center mt-8">
        <button
          onClick={() => navigate("/")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
        >
          ← Back to Homepage
        </button>
      </div>

      <div className="text-center mt-10">
        <h2 className="text-2xl font-bold text-indigo-600">🏆 Predicted NBA Champion: {bracket.Champion}</h2>
      </div>
    </div>
  );
}
