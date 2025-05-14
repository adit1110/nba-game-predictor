import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-blue-900 text-white shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-4 py-3">
        {/* Left: NBA Logo + Title */}
        <div className="flex items-center space-x-3">
          <img
  src="/NBA_logo.png"
  alt="NBA"
  style={{ maxWidth: '40px', maxHeight: '40px', width: 'auto', height: 'auto' }}
  className="object-contain"
/>

          <h1 className="text-2xl font-bold tracking-wider">NBA Predictor</h1>
        </div>

        {/* Right: Navigation */}
        <div className="hidden md:flex space-x-4">
          <button
            onClick={() => navigate('/')}
            className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded transition"
          >
            Home
          </button>
          <button
            onClick={() => navigate('/result')}
            className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded transition"
          >
            Results
          </button>
          <button
            onClick={() => navigate('/playoffs')}
            className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded transition"
          >
            Playoffs
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      <div className="md:hidden flex justify-center space-x-4 py-2 bg-blue-800">
        <button
          onClick={() => navigate('/')}
          className="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1 rounded transition"
        >
          Home
        </button>
        <button
          onClick={() => navigate('/result')}
          className="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1 rounded transition"
        >
          Results
        </button>
        <button
          onClick={() => navigate('/playoffs')}
          className="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1 rounded transition"
        >
          Playoffs
        </button>
      </div>
    </header>
  );
};

export default Header;
