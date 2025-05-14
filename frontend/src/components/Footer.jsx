import React from 'react';

const Footer = () => (
  <footer className="bg-blue-900 text-white py-4 mt-12">
    <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between px-4">
      <div className="text-sm text-center md:text-left">
        © {new Date().getFullYear()} Adit Bhimani — NBA Predictor
      </div>

      <div className="mt-2 md:mt-0">
        <a
          href="https://github.com/adit1110"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-300 hover:text-blue-100 no-underline text-sm"
        >
          GitHub
        </a>
      </div>
    </div>
  </footer>
);

export default Footer;
