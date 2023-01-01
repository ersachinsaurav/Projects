import React from "react";

export default function About(props) {
  return (
    <>
      <h2 className="mb-3 mt-4">About Us</h2>
      <div className="accordion mb-5" id="accordionExample">
        <div
          className="accordion-item"
          style={{
            backgroundColor: "dark" === props.themeMode ? "black" : "",
            color: "dark" === props.themeMode ? "white" : "",
          }}
        >
          <h2 className="accordion-header" id="headingOne">
            <button
              className="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseOne"
              aria-expanded="true"
              aria-controls="collapseOne"
              style={{
                backgroundColor: "dark" === props.themeMode ? "#212529" : "",
                color: "dark" === props.themeMode ? "white" : "",
              }}
            >
              <strong>Analyze Your Text</strong>
            </button>
          </h2>
          <div
            id="collapseOne"
            className="accordion-collapse collapse show"
            aria-labelledby="headingOne"
            data-bs-parent="#accordionExample"
          >
            <div className="accordion-body">
              TextUtils gives you a way to analyze your text quickly and
              efficiently. Be it word count or character count. TextUtils also
              gives the approximate time you will take to read the entered text.
            </div>
          </div>
        </div>
        <div
          className="accordion-item"
          style={{
            backgroundColor: "dark" === props.themeMode ? "black" : "",
            color: "dark" === props.themeMode ? "white" : "",
          }}
        >
          <h2 className="accordion-header" id="headingTwo">
            <button
              className="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseTwo"
              aria-expanded="false"
              aria-controls="collapseTwo"
              style={{
                backgroundColor: "dark" === props.themeMode ? "#212529" : "",
                color: "dark" === props.themeMode ? "white" : "",
              }}
            >
              <strong>Free To Use</strong>
            </button>
          </h2>
          <div
            id="collapseTwo"
            className="accordion-collapse collapse"
            aria-labelledby="headingTwo"
            data-bs-parent="#accordionExample"
          >
            <div className="accordion-body">
              TextUtils is a free character counter tool that provides instant
              character count & word count statistics for a given text.
              TextUtils reports the number of words and characters. Thus it is
              suitable for writing text with word or character limit.
            </div>
          </div>
        </div>
        <div
          className="accordion-item"
          style={{
            backgroundColor: "dark" === props.themeMode ? "black" : "",
            color: "dark" === props.themeMode ? "white" : "",
          }}
        >
          <h2 className="accordion-header" id="headingThree">
            <button
              className="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseThree"
              aria-expanded="false"
              aria-controls="collapseThree"
              style={{
                backgroundColor: "dark" === props.themeMode ? "#212529" : "",
                color: "dark" === props.themeMode ? "white" : "",
              }}
            >
              <strong>Browser Compatible</strong>
            </button>
          </h2>
          <div
            id="collapseThree"
            className="accordion-collapse collapse"
            aria-labelledby="headingThree"
            data-bs-parent="#accordionExample"
          >
            <div className="accordion-body">
              This word counter software works in any web browsers such as
              Chrome, Firefox, Internet Explorer, Safari, Opera. It suits to
              count characters in facebook, blog, books, excel document, pdf
              document, essays, etc.
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
