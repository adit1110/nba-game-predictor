import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => (
  <header className="bg-blue-900 text-white shadow-md">
    <div className="py-4 text-center">
      <h1 className="text-3xl tracking-widest">NBA Matchup Predictor</h1>
    </div>
    <nav className="flex justify-center space-x-6 py-2 bg-blue-800 text-sm">
      <Link to="/" className="hover:underline">Home</Link>
      <Link to="/result" className="hover:underline">Results</Link>
      <Link to="/playoffs" className="hover:underline">Playoffs</Link> {/* ✅ Added this */}
    </nav>
  </header>
);

export default Header;
