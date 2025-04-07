import React from 'react';
import Hero from './Hero';
import AboutUs from './About';
import LawPage from './LawPage';
import HelpSupportWidget from './HelpSupportWidget';

const CivilianDashboard = () => {
  return (
    <div>
      <Hero />
      <AboutUs />
      <LawPage />
      <HelpSupportWidget />
    </div>
  );
};

export default CivilianDashboard;