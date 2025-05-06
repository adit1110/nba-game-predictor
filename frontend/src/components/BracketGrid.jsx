import React from 'react';

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

const rounds = ["West Semis", "West Finals", "NBA Finals", "East Finals", "East Semis"];

const BracketGrid = ({ data }) => {
  if (!data?.Rounds) return <div className="text-center">No bracket data available.</div>;

  const getMatchupBlock = (game, isWinner) => {
    return (
      <div
        className={`w-44 flex flex-col items-center gap-2 p-2 rounded-lg shadow-sm transition
          ${isWinner ? "bg-green-100" : "bg-gray-100 opacity-50"} 
          hover:opacity-100 hover:bg-blue-50 relative group`}
      >
        <img
          src={`https://cdn.nba.com/logos/nba/${teamIdMap[isWinner ? game.winner : (game.winner === game.home ? game.away : game.home)]}/global/L/logo.svg`}
          alt="logo"
          className="w-10 h-10 object-contain"
        />
        <span className="font-bold">{isWinner ? game.winner : (game.winner === game.home ? game.away : game.home)}</span>

        <div className="absolute bg-black text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 top-full mt-1 whitespace-nowrap z-10">
          Confidence: {game.confidence.toFixed(2)}%
        </div>
      </div>
    );
  };

  const gridClasses = "grid grid-cols-5 gap-x-10 items-start";

  return (
    <div className="overflow-x-auto px-4 py-8">
      <h2 className="text-3xl text-center font-extrabold text-blue-800 mb-6">🏀 Visual NBA Bracket</h2>

      <div className={gridClasses}>
        {rounds.map((roundKey, colIndex) => (
          <div key={roundKey} className="space-y-6">
            <h3 className="text-center font-bold text-sm text-indigo-700">{roundKey}</h3>
            {data.Rounds[roundKey]?.map((game, i) => (
              <div key={i} className="space-y-1">
                {getMatchupBlock(game, false)}
                {getMatchupBlock(game, true)}
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Champion */}
      {data.Champion && (
        <div className="mt-10 text-center">
          <h2 className="text-2xl font-bold text-green-700">🏆 NBA Champion: {data.Champion}</h2>
        </div>
      )}
    </div>
  );
};

export default BracketGrid;
