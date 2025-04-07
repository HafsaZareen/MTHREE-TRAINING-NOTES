import React, { useState } from "react";
import axios from "axios";
import auth_bg from "../../assets/auth_bg.jpg";
import { useNavigate } from "react-router-dom";

const SignupForm = ({ userType: initialUserType }) => {
  const [userType, setUserType] = useState(initialUserType || "Civilian");
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    phoneno: "",
    password: "",
    confirmPassword: "",
    id: "",
  });
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleUserTypeChange2 = (type) => {
    setUserType(type);
    navigate(`/signup/${type.toLowerCase()}`);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    const phoneRegex = /^[0-9]{10}$/;
    if (!formData.email || !formData.password || !formData.phoneno) {
      setMessage("Please fill in all required fields");
      return false;
    }
    if (!phoneRegex.test(formData.phoneno)) {
      setMessage("Invalid phone number format");
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setMessage("Passwords don't match!");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!validateForm()) return;

    setIsLoading(true);
    try {
      const payload = {
        email: formData.email,
        phoneno: formData.phoneno,
        password: formData.password,
        ...(userType === "Civilian" ? { username: formData.username } : { id: formData.id }),
      };

      const response = await axios.post(
        `http://127.0.0.1:5000/api/${userType.toLowerCase()}/signup`,
        payload,
        { timeout: 10000 }
      );

      setMessage(response.data.message || "Signup successful! Please login.");
      setFormData({
        username: "",
        email: "",
        phoneno: "",
        password: "",
        confirmPassword: "",
        id: "",
      });
      setTimeout(() => navigate(`/login/${userType.toLowerCase()}`), 2000);
    } catch (error) {
      setMessage(error.response?.data?.message || "Signup failed. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="vh-100" style={{ backgroundColor: "#5C7285" }}>
      <div className="container py-5 h-100">
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="col col-xl-10">
            <div className="card" style={{ borderRadius: "1rem", backgroundColor: "#DBDBDB" }}>
              <div className="row g-0">
                <div className="col-md-6 col-lg-5 d-none d-md-block">
                  <img src={auth_bg} alt="signup" className="img-fluid" style={{ borderRadius: "1rem 0 0 1rem", height: "100%", width: "100%", objectFit: "cover" }} />
                </div>
                <div className="col-md-6 col-lg-7 d-flex align-items-center">
                  <div className="card-body p-4 p-lg-5 text-black">
                    <form onSubmit={handleSubmit}>
                      <div className="d-flex align-items-center mb-3 pb-1">
                        <span className="h1 fw-bold mb-0 text-info">IPC Nexus</span>
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Select User Type</label>
                        <div className="dropdown">
                          <button className="btn btn-outline-info dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {userType} Signup
                          </button>
                          <ul className="dropdown-menu">
                            {["Civilian", "Lawyer", "Police"].map((type) => (
                              <li key={type}>
                                <button className="dropdown-item" onClick={() => handleUserTypeChange2(type)}>
                                  {type} Signup
                                </button>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      {userType === "Civilian" && (
                        <div className="form-outline mb-4">
                          <input type="text" className="form-control form-control-lg" name="username" value={formData.username} onChange={handleChange} placeholder="Enter your username" required />
                        </div>
                      )}
                      {(userType === "Lawyer" || userType === "Police") && (
                        <div className="form-outline mb-4">
                          <input type="text" className="form-control form-control-lg" name="id" value={formData.id} onChange={handleChange} placeholder={`Enter your ${userType === "Lawyer" ? "Lawyer ID" : "Badge ID"}`} required />
                        </div>
                      )}
                      <div className="form-outline mb-4">
                        <input type="email" className="form-control form-control-lg" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" required />
                      </div>
                      <div className="form-outline mb-4">
                        <input type="tel" className="form-control form-control-lg" name="phoneno" value={formData.phoneno} onChange={handleChange} placeholder="Enter your phone number" required />
                      </div>
                      <div className="form-outline mb-4">
                        <input type="password" className="form-control form-control-lg" name="password" value={formData.password} onChange={handleChange} placeholder="Enter your password" required />
                      </div>
                      <div className="form-outline mb-4">
                        <input type="password" className="form-control form-control-lg" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} placeholder="Confirm password" required />
                      </div>
                      <div className="pt-1 mb-4">
                        <button className="btn btn-dark btn-lg btn-block" type="submit" disabled={isLoading}>
                          {isLoading ? "Signing up..." : "Sign Up"}
                        </button>
                      </div>
                      {message && <p className="mt-3 text-center text-danger">{message}</p>}
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SignupForm;