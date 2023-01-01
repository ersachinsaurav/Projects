import React, { useState } from "react";

export default function TextForm(props) {
  const [text, setText] = useState("");
  let textBoxPH = "Enter text here..";

  const handleUpperBtn = () => {
    if( "" !== text) {
      setText(text.toUpperCase());
      props.handleAlert("Text has been converted to uppercase.", "success");
    }
  };

  const handleLowerBtn = () => {
    if( "" !== text) {
      setText(text.toLowerCase());
      props.handleAlert("Text has been converted to lowercase.", "success");
    }
  };

  const handleClearBtn = () => {
    if( "" !== text) {
      setText("");
      props.handleAlert("TextBox has been cleared.", "success");
    }
  };

  const handleOnTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <>
      <div>
        <h2 className="mt-4"> {props.heading} </h2>
        <div className="mb-3">
          <textarea
            className="form-control"
            id="textBox"
            value={text}
            onChange={handleOnTextChange}
            placeholder={textBoxPH}
            rows="7"
            style={{
              backgroundColor: "dark" === props.themeMode ? "#212529" : "",
              color: "dark" === props.themeMode ? "white" : "",
            }}
          ></textarea>
        </div>
        <button className="btn btn-primary" onClick={handleUpperBtn}>
          {" "}
          =&gt; UPPERCASE
        </button>
        <button className="btn btn-primary m-3" onClick={handleLowerBtn}>
          {" "}
          =&gt; lowercase
        </button>
        <button className="btn btn-primary" onClick={handleClearBtn}>
          {" "}
          Clear
        </button>
      </div>
      <div className="mt-3">
        <h3>Text Summary:</h3>
        <p>
          You've entered {text.split(/\s+/).filter((x) => x !== "").length} words
          and {text.length} characters so far.
        </p>
        <p>
          It'll take {0.008 * text.split(/\s+/).filter((x) => x !== "").length}{" "}
          minutes to read.
        </p>
      </div>
    </>
  );
}
