import React, { useState } from 'react';
import axios from 'axios';
import '../styles/LoginInfo.css';
import states from '../states';

const PoliceInfo = () => {
  const [formData, setFormData] = useState({
    state: '',
    pinCode: '',
    stationNumber: '',
    stationLocation: '',
    policeId: '',
  });

  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');

  const validate = () => {
    let tempErrors = {};

    if (!formData.state.trim()) tempErrors.state = 'State is required';
    if (!formData.stationLocation.trim()) tempErrors.stationLocation = 'Station Location is required';
    if (!formData.pinCode) tempErrors.pinCode = 'Pin Code is required';
    else if (!/^\d+$/.test(formData.pinCode)) tempErrors.pinCode = 'Pin Code must be a number';
    if (!formData.stationNumber) tempErrors.stationNumber = 'Station Number is required';
    else if (!/^\d+$/.test(formData.stationNumber)) tempErrors.stationNumber = 'Station Number must be a number';
    if (!formData.policeId) tempErrors.policeId = 'Police ID is required';
    else if (!/^\d+$/.test(formData.policeId)) tempErrors.policeId = 'Police ID must be a number';

    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    if (validate()) {
      try {
        const response = await axios.post('http://localhost:5000/api/policeInfo', formData);
        setMessage(response.data.message || 'Data submitted successfully!');
        setFormData({
          state: '',
          pinCode: '',
          stationNumber: '',
          stationLocation: '',
          policeId: '',
        });
        setErrors({});
      } catch (error) {
        setMessage(error.response?.data?.message || 'Submission failed.');
      }
    }
  };

  return (
    <section className="vh-100 bg-custom">
      <div className="container py-5 h-100">
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="col-12 col-md-8 col-lg-6 col-xl-5">
            <div className="card bg-dark text-white" style={{ borderRadius: '1rem' }}>
              <div className="card-body p-5 text-center">
                <h2 className="fw-bold mb-2 text-uppercase">Registered Police-Station Information</h2>
                <p className="text-white-50 mb-5">Please enter your details below</p>

                <form onSubmit={handleSubmit}>
                  <div className="form-outline form-white mb-3">
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
                    {errors.state && <small className="text-danger">{errors.state}</small>}
                  </div>

                  <div className="form-outline form-white mb-3">
                    <input
                      type="text"
                      id="pinCode"
                      className="form-control form-control-lg"
                      name="pinCode"
                      value={formData.pinCode}
                      onChange={handleChange}
                      placeholder="Pin Code"
                    />
                    {errors.pinCode && <small className="text-danger">{errors.pinCode}</small>}
                  </div>

                  <div className="form-outline form-white mb-3">
                    <input
                      type="text"
                      id="stationNumber"
                      className="form-control form-control-lg"
                      name="stationNumber"
                      value={formData.stationNumber}
                      onChange={handleChange}
                      placeholder="Station Number"
                    />
                    {errors.stationNumber && <small className="text-danger">{errors.stationNumber}</small>}
                  </div>

                  <div className="form-outline form-white mb-3">
                    <input
                      type="text"
                      id="stationLocation"
                      className="form-control form-control-lg"
                      name="stationLocation"
                      value={formData.stationLocation}
                      onChange={handleChange}
                      placeholder="Station Location"
                    />
                    {errors.stationLocation && <small className="text-danger">{errors.stationLocation}</small>}
                  </div>

                  <div className="form-outline form-white mb-3">
                    <input
                      type="text"
                      id="policeId"
                      className="form-control form-control-lg"
                      name="policeId"
                      value={formData.policeId}
                      onChange={handleChange}
                      placeholder="Police ID"
                    />
                    {errors.policeId && <small className="text-danger">{errors.policeId}</small>}
                  </div>

                  <button className="btn btn-outline-light btn-lg px-5" type="submit">
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

export default PoliceInfo;
