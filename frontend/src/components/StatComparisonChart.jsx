import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList
} from 'recharts';

// Add your team colors here
const teamColors = {
  ATL: "#E03A3E", // Atlanta Hawks
  BOS: "#007A33", // Boston Celtics
  BKN: "#000000", // Brooklyn Nets
  CHA: "#1D1160", // Charlotte Hornets
  CHI: "#CE1141", // Chicago Bulls
  CLE: "#860038", // Cleveland Cavaliers
  DAL: "#00538C", // Dallas Mavericks
  DEN: "#0E2240", // Denver Nuggets
  DET: "#C8102E", // Detroit Pistons
  GSW: "#1D428A", // Golden State Warriors
  HOU: "#CE1141", // Houston Rockets
  IND: "#002D62", // Indiana Pacers
  LAC: "#C8102E", // Los Angeles Clippers
  LAL: "#552583", // Los Angeles Lakers
  MEM: "#5D76A9", // Memphis Grizzlies
  MIA: "#98002E", // Miami Heat
  MIL: "#00471B", // Milwaukee Bucks
  MIN: "#0C2340", // Minnesota Timberwolves
  NOP: "#0C2340", // New Orleans Pelicans
  NYK: "#006BB6", // New York Knicks
  OKC: "#007AC1", // Oklahoma City Thunder
  ORL: "#0077C0", // Orlando Magic
  PHI: "#006BB6", // Philadelphia 76ers
  PHX: "#1D1160", // Phoenix Suns
  POR: "#E03A3E", // Portland Trail Blazers
  SAC: "#5A2D81", // Sacramento Kings
  SAS: "#C4CED4", // San Antonio Spurs
  TOR: "#CE1141", // Toronto Raptors
  UTA: "#002B5C", // Utah Jazz
  WAS: "#002B5C", // Washington Wizards
};


function StatComparisonChart({ homeStats, awayStats, homeTeam, awayTeam }) {
  const statOrder = ["PTS", "REB", "AST", "FG%"];

  const data = statOrder.map((stat) => ({
    name: stat,
    Home: homeStats[stat],
    Away: awayStats[stat],
  }));

  const homeColor = teamColors[homeTeam] || "#3B82F6"; // default blue
  const awayColor = teamColors[awayTeam] || "#EF4444"; // default red

  return (
    <div className="mt-8">
      <h2 className="text-lg mb-4 text-center">📊 Team Stat Comparison</h2>
  
      <div className="w-full max-w-4xl mx-auto">
        <div className="flex justify-center gap-24 mb-2 text-base">
          <span className="text-gray-700">{homeTeam}</span>
          <span className="text-gray-700">{awayTeam}</span>
        </div>
  
        <ResponsiveContainer width="95%" height={300}>
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend
              payload={[
                { value: "Home", type: "square", id: "home", color: homeColor },
                { value: "Away", type: "square", id: "away", color: awayColor }
              ]}
            />
            <Bar dataKey="Home" fill={homeColor} animationDuration={1000}>
              <LabelList dataKey="Home" position="top" />
            </Bar>
            <Bar dataKey="Away" fill={awayColor} animationDuration={1000}>
              <LabelList dataKey="Away" position="top" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );  
}

export default StatComparisonChart;
