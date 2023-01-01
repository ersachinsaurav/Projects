import "./App.css";
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Alert from "./components/Alert";
import Home from "./components/Home";
import About from "./components/About";
import Login from "./components/Login";
import Signup from "./components/Signup";
import NoteState from "./context/notes/NoteState";

function App() {
  const [alert, setAlert] = useState(null);

  const handleAlert = (alertMsg, alertType) => {
    setAlert({
      alertMsg: alertMsg,
      alertType: alertType,
    });
    setTimeout(() => {
      setAlert(null);
    }, 5000);
  };

  return (
    <>
      <NoteState>
        <Router>
          <Navbar handleAlert={handleAlert} />
          <Alert alert={alert} />
          <div className="container mt-5">
            <Routes>
              <Route
                exact
                path="/"
                element={<Home handleAlert={handleAlert} />}
              />
              <Route exact path="/about" element={<About />} />
              <Route
                exact
                path="/login"
                element={<Login handleAlert={handleAlert} />}
              />
              <Route
                exact
                path="/signup"
                element={<Signup handleAlert={handleAlert} />}
              />
            </Routes>
          </div>
        </Router>
      </NoteState>
    </>
  );
}

export default App;
