import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Signup = (props) => {
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    password: "",
    cPassword: "",
  });
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/api/auth/createuser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: userData.name,
        email: userData.email,
        password: userData.password,
      }),
    });
    const responseJSON = await response.json();

    if (true === responseJSON.status) {
      localStorage.setItem("authToken", responseJSON.authToken);
      navigate("/");
      props.handleAlert(responseJSON.message, "success");
    } else {
      props.handleAlert(responseJSON.message, "danger");
    }
  };

  const onChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <h2 className="mt-2 mb-4">Create An Account To Use CloudBook</h2>
      <form onSubmit={handleSignup}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">
            Name
          </label>
          <input
            type="name"
            className="form-control"
            id="name"
            name="name"
            placeholder="Name"
            value={userData.name}
            onChange={onChange}
            required
            minLength={3}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            placeholder="Email"
            value={userData.email}
            onChange={onChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            name="password"
            className="form-control"
            id="password"
            placeholder="Password"
            value={userData.password}
            onChange={onChange}
            required
            minLength={6}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="cPassword" className="form-label">
            Confirm Password
          </label>
          <input
            type="password"
            name="cPassword"
            className="form-control"
            id="cPassword"
            placeholder="Confirm Password"
            value={userData.cPassword}
            onChange={onChange}
            required
            minLength={6}
          />
        </div>
        <button
          type="submit"
          disabled={
            userData.name === "" ||
            userData.name.length < 3 ||
            userData.email === "" ||
            userData.password === "" ||
            userData.cPassword === "" ||
            userData.password.length < 6 ||
            userData.cPassword.length < 6 ||
            userData.cPassword !== userData.password
              ? true
              : false
          }
          className="btn btn-primary"
        >
          Signup
        </button>
      </form>
    </div>
  );
};

export default Signup;
