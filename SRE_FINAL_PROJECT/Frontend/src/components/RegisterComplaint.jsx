import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/RegCom.css';
import bg from "../assets/RegcomBG.jpg";

const RegisterComplaint = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    incidentDate: '',
    location: '',
    address: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    const userType = localStorage.getItem('userType');
    if (!isAuthenticated || userType !== 'Police') {
      setMessage('You must be logged in as a police officer to register a complaint.');
      setTimeout(() => navigate('/login/police'), 2000);
    }
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    const badgeId = localStorage.getItem('badge_id');
    if (!badgeId) {
      setMessage('Police badge ID not found. Please log in again.');
      setLoading(false);
      setTimeout(() => navigate('/login/police'), 2000);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/police/complaint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          badge_id: badgeId,
          timestamp: new Date().toISOString(),
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to submit complaint');

      setMessage('Complaint registered successfully! Case ID: ' + data.case_id);
      setFormData({ name: '', email: '', phone: '', incidentDate: '', location: '', address: '', description: '' });
    } catch (error) {
      setMessage('Error submitting complaint: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-police">
      <div className="container d-flex align-items-center justify-content-center h-100">
        <div className="card card-registration my-4" style={{ maxWidth: '80rem', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
          <div className="row g-0">
            <div className="col-lg-6 d-none d-lg-block">
              <img src={bg} alt="Register Complaint" className="img-fluid" style={{ borderTopLeftRadius: '.25rem', borderBottomLeftRadius: '.25rem', height: '100%', objectFit: "cover" }} />
            </div>
            <div className="col-lg-6">
              <div className="card-body p-5">
                {message && <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-success'} mb-4`}>{message}</div>}
                <form onSubmit={handleSubmit}>
                  <h3 className="mb-4 text-primary text-center">Register Complaint</h3>
                  {['name', 'email', 'phone', 'incidentDate', 'location', 'address'].map((field, index) => (
                    <div className="mb-4" key={index}>
                      <input
                        type={field === 'incidentDate' ? 'date' : 'text'}
                        placeholder={field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                        name={field}
                        value={formData[field]}
                        onChange={handleChange}
                        required
                        className="form-control form-control-lg"
                      />
                    </div>
                  ))}
                  <div className="mb-4">
                    <textarea
                      rows={6}
                      placeholder="Description of the Incident"
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      required
                      className="form-control form-control-lg"
                    />
                  </div>
                  <button type="submit" className="btn btn-primary w-100" disabled={loading}>{loading ? 'Submitting...' : 'Submit'}</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterComplaint;
