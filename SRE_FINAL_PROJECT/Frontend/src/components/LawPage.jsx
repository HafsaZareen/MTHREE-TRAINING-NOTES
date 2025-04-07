import React from "react";
import { useParams } from "react-router-dom";
import "../styles/LawPage.css";
import LawContent from "./LawContent";

const LawPage = () => {
  const { lawId } = useParams(); // Extract 'lawId' from the URL
  const lawData = LawContent[lawId];

  if (!lawData) {
    return <div>Law type not found. Please select a valid option from the menu.</div>;
  }

  return (
    <div className="page-wrapper">
      {/* Left Section - Image */}
      <div className="image-section"></div>

      {/* Right Section - Text Content */}
      <div className="text-section">
        <h1>{lawData.title}</h1>
        <p className="description">{lawData.description}</p>
        <h4>Key Aspects:</h4>
        <ul>
          {lawData.keyAspects.map((aspect, index) => (
            <li key={index}>{aspect}</li>
          ))}
        </ul>
        <p className="description">Examples: {lawData.examples}</p>
        <a href={lawData.link} className="btn" target="_blank" rel="noopener noreferrer">
          Learn More
        </a>
      </div>
    </div>
  );
};

export default LawPage;
