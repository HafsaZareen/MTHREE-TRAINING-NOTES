import React, { useState, useEffect } from "react";
import { Row, Col, Card, Form, Button, Image } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import "../styles/EvidenceReport.css";
import bg from "../assets/Evi_BG.jpg";

function EvidenceReport() {
  const [complaintId, setComplaintId] = useState("");
  const [submitterId, setSubmitterId] = useState("");
  const [submitterType, setSubmitterType] = useState("");
  const [evidenceFile, setEvidenceFile] = useState(null);
  const [evidenceList, setEvidenceList] = useState([]);
  const [isEvidenceVisible, setIsEvidenceVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    const userType = localStorage.getItem('userType');
    const badgeId = localStorage.getItem('badge_id');
    const lawyerId = localStorage.getItem('lawyer_id');

    if (!isAuthenticated || !['Police', 'Lawyer'].includes(userType)) {
      setErrorMessage('You must be logged in as a police officer or lawyer to access this page.');
      setTimeout(() => navigate('/login/police'), 2000);
      return;
    }

    if (userType === 'Police' && badgeId) {
      setSubmitterId(badgeId);
      setSubmitterType('police');
    } else if (userType === 'Lawyer' && lawyerId) {
      setSubmitterId(lawyerId);
      setSubmitterType('lawyer');
    }
  }, [navigate]);

  const fetchEvidence = async (caseId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/evidence/case/${caseId}`);
      if (response.ok) {
        const data = await response.json();
        setEvidenceList(data);
      } else {
        console.error("Failed to fetch evidence:", response.statusText);
        setErrorMessage("Failed to fetch evidence");
      }
    } catch (error) {
      console.error("Error fetching evidence:", error);
      setErrorMessage("Error fetching evidence");
    }
  };

  const handleCaseIdChange = (e) => {
    const caseId = e.target.value;
    setComplaintId(caseId);
    if (caseId) fetchEvidence(caseId); // Fetch evidence when case ID is entered
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    const formData = new FormData();
    formData.append("complaintId", complaintId);
    formData.append("submitterId", submitterId);
    formData.append("submitterType", submitterType);
    formData.append("evidenceFile", evidenceFile);

    try {
      const response = await fetch("http://localhost:5000/api/evidence", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        alert("Evidence submitted successfully!");
        setEvidenceList([...evidenceList, result.evidence]);
        setEvidenceFile(null);
      } else {
        setErrorMessage(result.message || "Failed to submit evidence");
      }
    } catch (error) {
      console.error("Error submitting evidence:", error);
      setErrorMessage("An error occurred while submitting evidence");
    }
  };

  return (
    <section style={{ backgroundColor: "#5C7285", minHeight: "100vh", paddingTop: "3rem" }}>
      <Row className="justify-content-center mx-0" style={{ height: "60%" }}>
        <Col xl={8}>
          <Card className="rounded-3 text-black h-100 d-flex flex-row">
            <Col lg={6} className="d-flex flex-column justify-content-center">
              <Card.Body className="p-md-4 mx-md-3">
                <h4 className="text-center mb-4">Submit Your Evidence</h4>
                <Form onSubmit={handleSubmit}>
                  <p>Please fill in the details below</p>
                  <Form.Group className="mb-3">
                    <Form.Control
                      type="text"
                      placeholder="Case ID"
                      value={complaintId}
                      onChange={handleCaseIdChange}
                      required
                    />
                  </Form.Group>
                  <Form.Group className="mb-3">
                    <Form.Control
                      type="text"
                      placeholder={submitterType === 'police' ? "Police ID" : "Lawyer ID"}
                      value={submitterId}
                      disabled
                    />
                  </Form.Group>
                  <Form.Group className="mb-3">
                    <Form.Control
                      type="file"
                      onChange={(e) => setEvidenceFile(e.target.files[0])}
                      required
                    />
                  </Form.Group>
                  {errorMessage && <p className="text-danger">{errorMessage}</p>}
                  <Button className="btn btn-primary btn-block gradient-custom-2 mb-3" type="submit">
                    Submit Evidence
                  </Button>
                </Form>
                <Button
                  variant="info"
                  onClick={() => setIsEvidenceVisible(!isEvidenceVisible)}
                  className="btn-block"
                >
                  {isEvidenceVisible ? "Hide Existing Evidence" : "Show Existing Evidence"}
                </Button>
              </Card.Body>
            </Col>
            <Col lg={6} className="d-flex align-items-center gradient-custom-2">
              <Image
                src={bg}
                alt="Evidence Background"
                fluid
                className="rounded"
                style={{ maxHeight: "100%", maxWidth: "100%" }}
              />
            </Col>
          </Card>
        </Col>
      </Row>

      {isEvidenceVisible && (
        <Row className="justify-content-center mx-0 mt-3">
          <Col xl={8}>
            <Card className="rounded-3 text-black">
              <Card.Body className="p-md-4 mx-md-3">
                <h4 className="text-center mb-3">Existing Evidence</h4>
                {evidenceList.length > 0 ? (
                  <ul className="list-group">
                    {evidenceList.map((evidence, index) => (
                      <li
                        key={evidence.evidence_id || index}
                        className="list-group-item d-flex justify-content-between align-items-center"
                      >
                        <span>{`Evidence ${index + 1}:`}</span>
                        <span>{evidence.details}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-center">No evidence submitted yet for this case.</p>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </section>
  );
}

export default EvidenceReport;