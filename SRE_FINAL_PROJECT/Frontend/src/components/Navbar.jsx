import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Components.css';

const Navbar = ({ branches, userType }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('isAuthenticated') === 'true');
  const [username, setUsername] = useState(localStorage.getItem('username') || 'User');

  useEffect(() => {
    const handleStorageChange = () => {
      setIsAuthenticated(localStorage.getItem('isAuthenticated') === 'true');
      setUsername(localStorage.getItem('username') || 'User');
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-black shadow-sm">
      <div className="container">
        <Link className="navbar-brand fw-bold fs-4 text-info" to="/">
          IPC Nexus
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            {/* Laws Dropdown - Visible for all */}
            <li className="nav-item dropdown">
              <Link
                className="nav-link dropdown-toggle text-white"
                to="#"
                id="branchesDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
                style={{ transition: 'color 0.3s ease' }}
                onMouseEnter={(e) => (e.target.style.color = 'lightblue')}
                onMouseLeave={(e) => (e.target.style.color = 'white')}
              >
                Laws
              </Link>
              <ul className="dropdown-menu bg-black border-0" aria-labelledby="branchesDropdown">
                {branches.map((branch, index) => (
                  <li key={index}>
                    <Link
                      className="dropdown-item text-white"
                      to={`/${branch.toLowerCase().replace(/\s/g, '-')}`}
                      style={{ transition: 'color 0.3s ease' }}
                      onMouseEnter={(e) => (e.target.style.color = 'lightblue')}
                      onMouseLeave={(e) => (e.target.style.color = 'white')}
                    >
                      {branch}
                    </Link>
                  </li>
                ))}
              </ul>
            </li>

            {/* About Us - Visible for all */}
            <li className="nav-item">
              <Link className="nav-link text-white" to="/about">
                About Us
              </Link>
            </li>

            {/* Civilian Links */}
            {userType === 'Civilian' && isAuthenticated && (
              <>
           
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/IPCSections">
                    IPC Sections
                  </Link>
                </li>
            
              </>
            )}

            {/* Lawyer Links */}
            {userType === 'Lawyer' && isAuthenticated && (
              <>
              
             
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/IPCSections">
                    IPC Sections
                  </Link>
                </li>
              
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/caseInfo">
                    Case Info
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/lawyerinfo">
                    Lawyer Info
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/EvidenceReport">
                    Evidence Report
                  </Link>
                </li>
            
              </>
            )}

            {/* Police Links */}
            {userType === 'Police' && isAuthenticated && (
              <>
               
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/register-complaint">
                    Register Complaint
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/IPCSections">
                    IPC Sections
                  </Link>
                </li>
               
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/EvidenceReport">
                    Evidence Report
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/caseInfo">
                    Case Info
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/policeinfo">
                    Police Info
                  </Link>
                </li>
             
              </>
            )}
          </ul>

          {isAuthenticated ? (
            <div className="d-flex align-items-center">
              <span className="text-white me-3">Hi, {username}</span>
              <button
                className="btn btn-outline-danger"
                onClick={() => {
                  localStorage.removeItem('isAuthenticated');
                  localStorage.removeItem('userType');
                  localStorage.removeItem('username');
                  localStorage.removeItem('badge_id'); 
                  window.location.href = '/login/civilian';
                }}
              >
                Logout
              </button>
            </div>
          ) : (
            <>
              <div className="dropdown">
                <button
                  className="btn btn-outline-info dropdown-toggle me-2"
                  type="button"
                  id="loginDropdown"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Login
                </button>
                <ul className="dropdown-menu dropdown-menu-end bg-black border-0" aria-labelledby="loginDropdown">
                  <li><Link className="dropdown-item text-white" to="/login/civilian">Civilian Login</Link></li>
                  <li><Link className="dropdown-item text-white" to="/login/lawyer">Lawyer Login</Link></li>
                  <li><Link className="dropdown-item text-white" to="/login/police">Police Login</Link></li>
                </ul>
              </div>
              <div className="dropdown">
                <button
                  className="btn btn-outline-info dropdown-toggle me-2"
                  type="button"
                  id="signupDropdown"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Signup
                </button>
                <ul className="dropdown-menu dropdown-menu-end bg-black border-0" aria-labelledby="signupDropdown">
                  <li><Link className="dropdown-item text-white" to="/signup/civilian">Civilian Signup</Link></li>
                  <li><Link className="dropdown-item text-white" to="/signup/lawyer">Lawyer Signup</Link></li>
                  <li><Link className="dropdown-item text-white" to="/signup/police">Police Signup</Link></li>
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;