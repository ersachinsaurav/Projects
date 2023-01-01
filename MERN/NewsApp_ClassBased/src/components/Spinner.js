import React, { Component } from "react";
import spinner from "./loader.gif";

export class Spinner extends Component {
  render() {
    return (
      <div className="h-100 d-flex align-items-center justify-content-center my-3">
        <img src={spinner} alt="Loading" />
      </div>
    );
  }
}

export default Spinner;
