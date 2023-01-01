import React from "react";
import Notes from "./Notes";

const Home = (props) => {
  return (
    <>
      {localStorage.getItem("authToken") ? (
        <Notes handleAlert={props.handleAlert} />
      ) : (
        <div>Home</div>
      )}
    </>
  );
};

export default Home;
