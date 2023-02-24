import React, { useState, useEffect } from "react";
import {
  fetchContest,
  addNewNameToContest,
} from "../api-client";
import Header from "./Header";

const Contest = ({ initialContest, onContestListClick }) => {
  const [contest, setContest] = useState(initialContest);

  const handleClickContestList = (event) => {
    event.preventDefault();
    onContestListClick();
  };

  const handleNewNameSubmit = async (event) => {
    event.preventDefault();
    const newName = event.target.newName;
    const updatedContest = await addNewNameToContest({
      contestId: contest.id,
      newName: newName.value,
    });
    setContest(updatedContest);
    event.target.reset();
  };

  useEffect(() => {
    if (!contest.names) {
      fetchContest(contest.id).then((contest) => {
        setContest(contest);
      });
    }
  }, [contest.id, contest.names]);

  return (
    <>
      <Header message={contest.contestName} />
      <div className="contest">
        <div className="title">Contest Description</div>
        <div className="description">{contest.description}</div>

        <div className="title">Proposed Names</div>
        <div className="body">
          {contest.names?.length > 0 ? (
            <div className="list">
              {contest.names.map((proposedName) => (
                <div key={proposedName.id} className="item">
                  {proposedName.name}
                </div>
              ))}
            </div>
          ) : (
            <div>No Name Proposed Yet.</div>
          )}
        </div>

        <div className="title">Propose A New Name</div>
        <div className="body">
          <form onSubmit={handleNewNameSubmit}>
            <input
              type="text"
              name="newName"
              id="newName"
              placeholder="New Name Here"
            />
            <button type="submit">Submit</button>
          </form>
        </div>

        <a
          href="/"
          className="link"
          onClick={handleClickContestList}
        >
          Contest List
        </a>
      </div>
    </>
  );
};

export default Contest;
