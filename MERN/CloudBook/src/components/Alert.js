import React from "react";

function Alert(props) {
  const capitalize = (word) => {
    return word == "danger"
      ? "Error"
      : word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  };

  return (
    <div style={{ height: "43px" }}>
      {props.alert && (
        <div
          className={`alert alert-${props.alert.alertType} alert-dismissible fade show`}
          role="alert"
        >
          <strong>{capitalize(props.alert.alertType)}: </strong>{" "}
          {props.alert.alertMsg}
        </div>
      )}
    </div>
  );
}

export default Alert;
