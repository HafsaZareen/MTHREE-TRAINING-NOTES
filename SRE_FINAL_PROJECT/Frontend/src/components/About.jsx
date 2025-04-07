import React from "react";
import "../styles/About.css";
import abbg from "../assets/abbg.jpg";

const AboutUs = () => {
  return (
    <div className="container-fluid about-container">
      <div className="row align-items-center">
        {/* Left Side: Text Section */}
        <div className="col-md-6 text-container">
          <h1>About Us</h1>
          <p className="lead">
            Welcome to our platform, where we provide valuable learning resources
            on various subjects, including legal references for police officers
            and criminal law insights for public awareness.
          </p>
          <h2>Our Mission</h2>
          <p>
            Our mission is to ensure that police officers, legal professionals,
            and the general public have quick and easy access to crucial IPC sections
            to aid in FIR filing, law enforcement, and understanding criminal laws.
          </p>
          <h2>Why This is Important</h2>
          <ul>
            <li>Ensures accurate legal information for FIRs.</li>
            <li>Reduces errors in legal documentation.</li>
            <li>Speeds up law enforcement processes.</li>
            <li>Empowers officers and the public with legal knowledge at their fingertips.</li>
            <li>Enhances legal literacy and helps individuals understand their rights.</li>
          </ul>
        </div>

        {/* Right Side: Image Section */}
        <div className="col-md-6 image-container">
  <img
    src={abbg}
    alt="About Us"
    className="img-fluid rounded shadow"
  />
</div>

      </div>
    </div>
  );
};

export default AboutUs;
