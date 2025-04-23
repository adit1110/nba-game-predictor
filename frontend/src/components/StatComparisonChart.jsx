import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function StatComparisonChart({ homeStats, awayStats }) {
  const data = Object.keys(homeStats).map((stat) => ({
    name: stat,
    Home: homeStats[stat],
    Away: awayStats[stat],
  }));

  return (
    <div className="mt-8">
      <h2 className="text-lg font-semibold mb-4">📊 Team Stat Comparison</h2>
      <div className='w-full max-w-4xl mx-auto'>
      <ResponsiveContainer width="95%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Home" fill="#4F46E5" />
          <Bar dataKey="Away" fill="#EF4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
    </div>
  );
}

export default StatComparisonChart;
