import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import HomePage from './pages/HomePage';
import ResultPage from './pages/Resultpage';
import PlayoffBracket from './pages/PlayoffBracket';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/playoffs" element={<PlayoffBracket />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
