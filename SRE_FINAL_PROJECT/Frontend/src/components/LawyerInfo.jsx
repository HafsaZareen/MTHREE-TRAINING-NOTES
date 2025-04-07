import React, { useState } from 'react';
import axios from 'axios';
import '../styles/LoginInfo.css';
import states from '../states.jsx'; // Import the states

const LawyerInfo = () => {
  const [formData, setFormData] = useState({
    barId: '',
    branchName: '',
    state: '',
    courtLocation: '',
    judiciary: '',
    judiciaryId: '',
  });

  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState(''); // Added state for message color

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/lawyerInfo', formData);
      setMessage(response.data.message || 'Data submitted successfully!');
      setMessageColor('green');
    } catch (error) {
      setMessage(error.response?.data?.message || 'Submission failed.');
      setMessageColor('red');
    }
  };

  return (
    <section className="vh-100 bg-custom">
      <div className="container py-5 h-100">
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="col-12 col-md-8 col-lg-6 col-xl-5">
            <div className="card bg-dark text-white" style={{ borderRadius: '1rem' }}>
              <div className="card-body p-5 text-center">
                { <h2 className="fw-bold mb-2 text-uppercase">Court Information</h2> /*to store the court information, with whoom the lawyer is registered */}
                <p className="text-white-50 mb-5">Please enter your details below</p>

                <form onSubmit={handleSubmit}>
                  <div className="form-outline form-white mb-4">
                    <input
                      type="text"
                      id="barId"
                      className="form-control form-control-lg"
                      name="barId"
                      value={formData.barId}
                      onChange={handleChange}
                      placeholder="Bar ID"
                    />
                  </div>

                  <div className="form-outline form-white mb-4">
                    <input
                      type="text"
                      id="branchName"
                      className="form-control form-control-lg"
                      name="branchName"
                      value={formData.branchName}
                      onChange={handleChange}
                      placeholder="Branch Name"
                    />
                  </div>

                  <div className="form-outline form-white mb-4">
                    <select
                      id="state"
                      className="form-control form-control-lg"
                      name="state"
                      value={formData.state}
                      onChange={handleChange}
                    >
                      <option value="">Select State</option>
                      {states.map((state, index) => (
                        <option key={index} value={state}>
                          {state}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-outline form-white mb-4">
                    <input
                      type="text"
                      id="courtLocation"
                      className="form-control form-control-lg"
                      name="courtLocation"
                      value={formData.courtLocation}
                      onChange={handleChange}
                      placeholder="Court Location"
                    />
                  </div>

                  <div className="form-outline form-white mb-4">
                    <input
                      type="text"
                      id="judiciary"
                      className="form-control form-control-lg"
                      name="judiciary"
                      value={formData.judiciary}
                      onChange={handleChange}
                      placeholder="Judiciary"
                    />
                  </div>

                  <div className="form-outline form-white mb-4">
                    <input
                      type="text"
                      id="judiciaryId"
                      className="form-control form-control-lg"
                      name="judiciaryId"
                      value={formData.judiciaryId}
                      onChange={handleChange}
                      placeholder="Judiciary ID"
                    />
                  </div>

                  <button
                    className="btn btn-outline-light btn-lg px-5"
                    type="submit"
                  >
                    Submit
                  </button>
                </form>

                {message && (
                  <p className="mt-3">
                    <span className={message.includes('successfully') ? 'text-success' : 'text-danger'}>
                      {message}
                    </span>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LawyerInfo;
