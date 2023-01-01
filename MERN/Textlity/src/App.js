import "./App.css";
import About from "./components/About";
import Navbar from "./components/Navbar";
import TextForm from "./components/TextForm";
import React, { useState } from "react";
import Alert from "./components/Alert";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  const [themeMode, setThemeMode] = useState("light");
  const [alert, setAlert] = useState(null);

  const handleAlert = (alertMsg, alertType) => {
    setAlert({
      alertMsg: alertMsg,
      alertType: alertType,
    });
    setTimeout(() => {
      setAlert(null);
    }, 2000);
  };

  const handleModeBtnClick = () => {
    if ("light" === themeMode) {
      setThemeMode("dark");
      document.body.style.backgroundColor = "black";
      document.body.style.color = "white";
      handleAlert("Dark Mode has been enabled.", "success");
    } else {
      setThemeMode("light");
      document.body.style.backgroundColor = "";
      document.body.style.color = "";
      handleAlert("Light Mode has been enabled.", "success");
    }
  };

  return (
    <>
      <Router>
        <Navbar
          title="TextUtils"
          aboutText="About Us"
          themeMode={themeMode}
          handleModeBtnClick={handleModeBtnClick}
        />
        <div className="container mt-5">
          <Alert alert={alert} />
          <Routes>
            <Route
              exact
              path="/"
              element={
                <TextForm
                  heading="Enter Text"
                  themeMode={themeMode}
                  handleAlert={handleAlert}
                />
              }
            />
            <Route
              exact
              path="/about"
              element={<About themeMode={themeMode} />}
            />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
