import React from 'react';

const Footer = () => (
  <footer className="bg-blue-900 text-white text-center py-2 mt-12">
    <p className="text-sm">
      © {new Date().getFullYear()} Adit Bhimani |{' '}
      <a href="https://github.com/adit1110" className="underline">GitHub</a>
    </p>
  </footer>
);

export default Footer;
