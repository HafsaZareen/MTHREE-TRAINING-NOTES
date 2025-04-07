import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Footer from './components/Footer';
import RegisterComplaint from './components/RegisterComplaint';
import IPCSectionsTable from './components/Learn_IPC';
import LawPage from './components/LawPage';
import AboutUs from './components/About';
import ComplaintHistory from './components/ComplaintHistory';
import HelpSupportWidget from './components/HelpSupportWidget';
import LoginForm from './components/UserAuth/LoginForm';
import SignupForm from './components/UserAuth/SignupForm';
import EvidenceReport from './components/EvidenceReport';
import CaseInfo from './components/CaseInfo';
import LawyerInfo from './components/LawyerInfo';
import PoliceInfo from './components/PoliceInfo';
import CivilianDashboard from './components/CivilianDashboard';
import PoliceDashboard from './components/PoliceDashboard';
import LawyerDashboard from './components/LawyerDashboard';
import './App.css';

const ProtectedRoute = ({ element, userType }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  const currentUserType = localStorage.getItem('userType');
  return isAuthenticated && (!userType || currentUserType === userType) ? (
    element
  ) : (
    <Navigate to="/login/civilian" replace />
  );
};

function App() {
  const branches = ['Civil', 'Patent', 'Criminal', 'Family Law', 'Labour Law'];
  const [userType, setUserType] = useState(localStorage.getItem('userType') || null);

  useEffect(() => {
    const handleStorageChange = () => setUserType(localStorage.getItem('userType') || null);
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return (
    <Router>
      <Navbar branches={branches} userType={userType} />
      <Routes>
        <Route path="/" element={<><Hero /><Features /><Footer /><HelpSupportWidget /></>} />
        <Route path="/home" element={<><Hero /><Features /><Footer /><HelpSupportWidget /></>} />

        {/* Auth Routes */}
        <Route path="/signup/civilian" element={<><SignupForm userType="Civilian" /><HelpSupportWidget /></>} />
        <Route path="/signup/lawyer" element={<><SignupForm userType="Lawyer" /><HelpSupportWidget /></>} />
        <Route path="/signup/police" element={<><SignupForm userType="Police" /><HelpSupportWidget /></>} />
        <Route path="/login/civilian" element={<><LoginForm userType="Civilian" /><HelpSupportWidget /></>} />
        <Route path="/login/lawyer" element={<><LoginForm userType="Lawyer" /><HelpSupportWidget /></>} />
        <Route path="/login/police" element={<><LoginForm userType="Police" /><HelpSupportWidget /></>} />

        {/* Protected Routes */}
        <Route path="/dashboard/civilian" element={<ProtectedRoute element={<><CivilianDashboard /><HelpSupportWidget /></>} userType="Civilian" />} />
        <Route path="/dashboard/police" element={<ProtectedRoute element={<><PoliceDashboard /><HelpSupportWidget /></>} userType="Police" />} />
        <Route path="/dashboard/lawyer" element={<ProtectedRoute element={<><LawyerDashboard /><HelpSupportWidget /></>} userType="Lawyer" />} />
        <Route path="/:lawId" element={<ProtectedRoute element={<><LawPage /><HelpSupportWidget /></>} />} />
        <Route path="/register-complaint" element={<ProtectedRoute element={<><RegisterComplaint /><HelpSupportWidget /></>} />} />
        <Route path="/complaint-history" element={<ProtectedRoute element={<><ComplaintHistory /><HelpSupportWidget /></>} />} />
        <Route path="/IPCSections" element={<ProtectedRoute element={<><IPCSectionsTable /><HelpSupportWidget /></>} />} />
        <Route path="/about" element={<><AboutUs /><HelpSupportWidget /></>} />
        <Route path="/caseInfo" element={<ProtectedRoute element={<><CaseInfo /><HelpSupportWidget /></>} />} />
        <Route path="/EvidenceReport" element={<ProtectedRoute element={<><EvidenceReport /><HelpSupportWidget /></>} />} />
        <Route path="/policeinfo" element={<ProtectedRoute element={<><PoliceInfo /><HelpSupportWidget /></>} />} />
        <Route path="/lawyerinfo" element={<ProtectedRoute element={<><LawyerInfo /><HelpSupportWidget /></>} />} />
      </Routes>
    </Router>
  );
}

export default App;