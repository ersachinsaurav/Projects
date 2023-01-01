import React from "react";
import spinner from "./loader.gif";

const Spinner = () => {
  return (
    <div className="h-100 d-flex align-items-center justify-content-center my-3">
      <img src={spinner} alt="Loading" />
    </div>
  );
};

export default Spinner;
