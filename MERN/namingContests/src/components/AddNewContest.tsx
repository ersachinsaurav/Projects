import { useState } from "react";
import { addContest } from "../api-client";

const AddNewContest = ({ onSuccess }) => {
  const [isFormVisible, setIsFormVisible] = useState(false);

  const handleAddContestFormSubmit = async (event) => {
    event.preventDefault();
    const contestForm = event.target;

    const newContestData = {
      contestName: contestForm.contestName.value,
      categoryName: contestForm.categoryName.value,
      description: contestForm.description.value,
    };

    const newContest = await addContest(newContestData);

    if (newContest?.id) {
      contestForm.reset();
      onSuccess(newContest);
    }
  };

  return (
    <>
      {!isFormVisible && (
        <div style={{ textAlign: "right", margin: "1rem" }}>
          <a
            className="link"
            onClick={() => setIsFormVisible(true)}
          >
            Add New Contest
          </a>
        </div>
      )}

      {isFormVisible && (
        <div
          id="contestForm"
          className="contest"
          style={{ margin: "1rem" }}
        >
          <div className="title">Add New Contest</div>
          <div className="body">
            <form onSubmit={handleAddContestFormSubmit}>
              <div className="row">
                <div className="column1">
                  <label htmlFor="contestName">
                    Contest Name:
                  </label>
                </div>
                <div className="column2">
                  <input
                    type="text"
                    name="contestName"
                    placeholder="Contest Name Here"
                  />
                </div>
              </div>

              <div className="row">
                <div className="column1">
                  <label htmlFor="categoryName">
                    Category Name:
                  </label>
                </div>
                <div className="column2">
                  <input
                    type="text"
                    name="categoryName"
                    placeholder="Contest Category Here"
                  />
                </div>
              </div>

              <div className="row">
                <div className="column1">
                  <label htmlFor="description">
                    Category Name:
                  </label>
                </div>
                <div className="column2">
                  <textarea
                    name="description"
                    placeholder="Contest Description Here"
                    rows="3"
                  ></textarea>
                </div>
              </div>
              <div className="submitContest">
                <button
                  type="button"
                  className="cancelBtn"
                  onClick={() => setIsFormVisible(false)}
                >
                  Cancel
                </button>
                <button type="submit">Submit</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default AddNewContest;
