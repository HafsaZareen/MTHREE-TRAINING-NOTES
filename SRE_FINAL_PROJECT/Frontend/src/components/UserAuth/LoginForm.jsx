import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import auth_bg from "../../assets/auth_bg.jpg";

const LoginForm = ({ userType: initialUserType }) => {
  const [formData, setFormData] = useState({
    idOrUsername: "",
    password: "",
  });
  const [userType, setUserType] = useState(initialUserType || "Civilian");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleUserTypeChange = (type) => {
    setUserType(type);
    navigate(`/login/${type.toLowerCase()}`);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    if (!formData.idOrUsername || !formData.password) {
      setMessage("Please fill in all required fields");
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
      const response = await axios.post(
        `http://127.0.0.1:5000/api/${userType.toLowerCase()}/login`,
        {
          idOrUsername: formData.idOrUsername,
          password: formData.password,
        },
        { timeout: 10000 }
      );

      const { message: successMessage, badge_id, civilian_id, account_id } = response.data;

      setMessage(successMessage || "Login successful!");

      if (successMessage.includes("successful")) {
        localStorage.setItem("userType", userType);
        localStorage.setItem("isAuthenticated", "true");
        localStorage.setItem("username", formData.idOrUsername); // Use idOrUsername as fallback

        // Store badge_id for Police, or other IDs if applicable
        if (userType === "Police" && badge_id) {
          localStorage.setItem("badge_id", badge_id);
        } else if (userType === "Civilian" && civilian_id) {
          localStorage.setItem("civilian_id", civilian_id);
        } else if (userType === "Lawyer") {
          localStorage.setItem("lawyer_id", formData.idOrUsername); // Assuming Lawyer ID is idOrUsername
        }

        const navigatePath = `/dashboard/${userType.toLowerCase()}`;
        navigate(navigatePath); // Redirect to dashboard
        window.location.reload();
      }
    } catch (error) {
      console.error("Login Error:", error);
      setMessage(
        error.response?.data?.message ||
        "Login failed. Please check your credentials."
      );
      setTimeout(() => navigate(`/signup/${userType.toLowerCase()}`), 2000);
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
                  <img
                    src={auth_bg}
                    alt="login"
                    className="img-fluid"
                    style={{
                      borderRadius: "1rem 0 0 1rem",
                      height: "100%",
                      width: "100%",
                      objectFit: "cover",
                    }}
                  />
                </div>
                <div className="col-md-6 col-lg-7 d-flex align-items-center">
                  <div className="card-body p-4 p-lg-5 text-black">
                    <div className="mb-3">
                      <label className="form-label">Select User Type</label>
                      <div className="dropdown">
                        <button
                          className="btn btn-outline-info dropdown-toggle"
                          type="button"
                          data-bs-toggle="dropdown"
                          aria-expanded="false"
                        >
                          {userType} Login
                        </button>
                        <ul className="dropdown-menu">
                          {["Civilian", "Lawyer", "Police"].map((type) => (
                            <li key={type}>
                              <button
                                className="dropdown-item"
                                onClick={() => handleUserTypeChange(type)}
                              >
                                {type} Login
                              </button>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <form onSubmit={handleSubmit}>
                      <h5 className="fw-normal mb-3 pb-3">Login as {userType}</h5>
                      <div className="form-outline mb-4">
                        <input
                          type="text"
                          className="form-control form-control-lg"
                          name="idOrUsername"
                          value={formData.idOrUsername}
                          onChange={handleChange}
                          placeholder={`Enter your ${userType === "Civilian" ? "Username" : userType === "Lawyer" ? "Lawyer ID" : "Badge ID"}`}
                          required
                        />
                      </div>
                      <div className="form-outline mb-4">
                        <input
                          type="password"
                          className="form-control form-control-lg"
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          placeholder="Enter your password"
                          required
                        />
                      </div>
                      <div className="pt-1 mb-4">
                        <button
                          className="btn btn-dark btn-lg btn-block"
                          type="submit"
                          disabled={isLoading}
                        >
                          {isLoading ? "Logging in..." : "Login"}
                        </button>
                      </div>
                      <div className="d-flex justify-content-between">
                        <a className="small text-muted" href="/forgot-password">
                          Forgot password?
                        </a>
                        <a className="small text-muted" href={`/signup/${userType.toLowerCase()}`}>
                          Don’t have an account? Sign up
                        </a>
                      </div>
                      {message && (
                        <p className={`mt-3 text-center ${message.includes("successful") ? "text-success" : "text-danger"}`}>
                          {message}
                        </p>
                      )}
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

export default LoginForm;