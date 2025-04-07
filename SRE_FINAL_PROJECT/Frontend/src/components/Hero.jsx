import React, { useState, useEffect } from 'react';
// import SearchBar from './SearchBar';
import CrimeSearch from './CrimeSearch';
import '../styles/Components.css';

const Hero = () => {
  const [animatedText, setAnimatedText] = useState('');
  const message = 'Welcome to IPC Nexus';

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      if (i <= message.length) {
        setAnimatedText(message.substring(0, i));
        i++;
      } else {
        clearInterval(interval);
      }
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="hero-container">
      <div className="hero-content">
        <div className="hero-text">
          <h1>{animatedText}</h1>
          <p className="hero-subtitle">Search Indian Penal Code Sections</p>
        </div>
        <div className="searchBar-container">
          <CrimeSearch />
        </div>
      </div>
    </div>
  );
};

export default Hero;
