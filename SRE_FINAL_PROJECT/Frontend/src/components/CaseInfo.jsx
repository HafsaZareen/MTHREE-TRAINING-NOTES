import React, { useState, useEffect } from "react";
import { Tabs, Tab, Container } from "react-bootstrap";
import "../styles/CaseInfo.css";

function CaseInfo() {
  const [key, setKey] = useState("assigned");
  const [assignedCases, setAssignedCases] = useState([]);
  const [resolvedCases, setResolvedCases] = useState([]);
  const userType = localStorage.getItem('userType');
  const badgeId = localStorage.getItem('badge_id');
  const lawyerId = localStorage.getItem('lawyer_id');

  useEffect(() => {
    const fetchCases = async () => {
      try {
        let url = '';
        if (userType === 'Police' && badgeId) {
          url = `http://localhost:5000/api/police/cases/${badgeId}`;
        } else if (userType === 'Lawyer' && lawyerId) {
          url = `http://localhost:5000/api/lawyer/cases/${lawyerId}`;
        } else {
          console.error("User not authenticated or invalid user type");
          return;
        }

        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          const data = await response.json();
          setAssignedCases(data.assignedCases || []);
          setResolvedCases(data.resolvedCases || []); // Only for police
        } else {
          console.error("Failed to fetch cases");
        }
      } catch (error) {
        console.error("Error fetching cases:", error);
      }
    };

    fetchCases();
  }, [userType, badgeId, lawyerId]);

  return (
    <div className="background-CaseInfo">
      <Container className="case-info-container">
        <div className="tab-container">
          <Tabs
            activeKey={key}
            onSelect={(k) => setKey(k)}
            className="mb-3 tabs"
            justify
          >
            <Tab eventKey="assigned" title={<strong>Assigned Cases</strong>}>
              <div className="tab-content">
                <h3>Assigned Cases</h3>
                {assignedCases.length > 0 ? (
                  assignedCases.map((caseItem) => (
                    <div key={caseItem.case_id} className="case-item">
                      <p className="case-text">
                        <strong>Case ID:</strong> {caseItem.case_id}<br />
                        <strong>Title:</strong> {caseItem.title}<br />
                        <strong>Description:</strong> {caseItem.description}<br />
                        <strong>Lawyer ID:</strong> {caseItem.lawyer_id || 'N/A'}
                      </p>
                    </div>
                  ))
                ) : (
                  <p className="no-cases-text">No assigned cases available.</p>
                )}
              </div>
            </Tab>
            {userType === 'Police' && (
              <Tab eventKey="resolved" title={<strong>Resolved Cases</strong>}>
                <div className="tab-content">
                  <h3>Resolved Cases</h3>
                  {resolvedCases.length > 0 ? (
                    resolvedCases.map((caseItem) => (
                      <div key={caseItem.case_id} className="case-item">
                        <p className="case-text">
                          <strong>Case ID:</strong> {caseItem.case_id}<br />
                          <strong>Title:</strong> {caseItem.title}<br />
                          <strong>Description:</strong> {caseItem.description}<br />
                          <strong>Lawyer ID:</strong> {caseItem.lawyer_id || 'N/A'}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="no-cases-text">No resolved cases available.</p>
                  )}
                </div>
              </Tab>
            )}
          </Tabs>
        </div>
      </Container>
    </div>
  );
}

export default CaseInfo;