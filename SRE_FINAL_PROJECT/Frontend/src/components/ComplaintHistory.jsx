import React, { useState, useEffect } from 'react';
import { Container, Card, Table, Badge, Spinner } from 'react-bootstrap';
import '../styles/Components.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
console.log('API_URL:', API_URL); // Debug log

const ComplaintHistory = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    console.log('Component mounted, fetching complaints...'); // Debug log
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    try {
      console.log('Making API request to:', `${API_URL}/api/complaints`); // Debug log
      const response = await fetch(`${API_URL}/api/complaints`);
      console.log('Response status:', response.status); // Debug log
      
      if (!response.ok) {
        throw new Error(`Failed to fetch complaints: ${response.status}`);
      }
      const data = await response.json();
      console.log('Received data:', data); // Debug log
      setComplaints(data);
    } catch (error) {
      console.error('Error details:', error); // Debug log
      setError('Error loading complaints. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Card className="text-center p-4">
          <h3 className="text-danger">{error}</h3>
        </Card>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <Card className="shadow-sm">
        <Card.Header className="bg-primary text-white">
          <h3 className="mb-0">Complaint History</h3>
        </Card.Header>
        <Card.Body>
          {complaints.length === 0 ? (
            <div className="text-center py-5">
              <h4>No complaints found</h4>
              <p className="text-muted">Be the first to register a complaint</p>
            </div>
          ) : (
            <div className="table-responsive">
              <Table hover className="mb-0">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Incident Date</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Registered On</th>
                  </tr>
                </thead>
                <tbody>
                  {complaints.map((complaint, index) => (
                    <tr key={index}>
                      <td>
                        <div>
                          <strong>{complaint.name}</strong>
                          <br />
                          <small className="text-muted">{complaint.email}</small>
                        </div>
                      </td>
                      <td>{formatDate(complaint.incident_date)}</td>
                      <td>{complaint.location}</td>
                      <td>
                        <Badge bg="warning">{complaint.status}</Badge>
                      </td>
                      <td>{formatDate(complaint.timestamp)}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ComplaintHistory; 