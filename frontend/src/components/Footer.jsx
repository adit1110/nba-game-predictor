import React from 'react';
import { useNavigate } from 'react-router-dom';

const Footer = () => {
  const navigate = useNavigate();

  return (
    <footer className="bg-blue-900 text-white py-4 mt-12">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between px-4">
        <div className="text-sm text-center md:text-left">
          © {new Date().getFullYear()} Adit Bhimani — NBA Predictor
        </div>
      </div>
    </footer>
  );
};

export default Footer;
