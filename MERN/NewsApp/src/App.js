import "./App.css";
import React, { useState } from "react";
import Navbar from "./components/Navbar";
import News from "./components/News";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoadingBar from "react-top-loading-bar";

const App = () => {
  const pageSize = 9;
  const apiKey = process.env.REACT_APP_API_KEY;
  const [progress, setProgress] = useState(0);

  return (
    <>
      <Router>
        <LoadingBar color={"#f11946"} height={5} progress={progress} />
        <Navbar />
        <Routes>
          <Route
            exact
            path="/"
            element={
              <News
                key={"general"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"general"}
              />
            }
          />
          <Route
            exact
            path="/business"
            element={
              <News
                key={"business"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"business"}
              />
            }
          />
          <Route
            exact
            path="/entertainment"
            element={
              <News
                key={"entertainment"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"entertainment"}
              />
            }
          />
          <Route
            exact
            path="/health"
            element={
              <News
                key={"health"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"health"}
              />
            }
          />
          <Route
            exact
            path="/science"
            element={
              <News
                key={"science"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"science"}
              />
            }
          />
          <Route
            exact
            path="/sports"
            element={
              <News
                key={"sports"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"sports"}
              />
            }
          />
          <Route
            exact
            path="/technology"
            element={
              <News
                key={"technology"}
                apiKey={apiKey}
                setProgress={setProgress}
                pageSize={pageSize}
                country={"in"}
                category={"technology"}
              />
            }
          />
        </Routes>
      </Router>
    </>
  );
};

export default App;
