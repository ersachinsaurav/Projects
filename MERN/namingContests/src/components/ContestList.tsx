import ContestPreview from "./ContestPreview";
import { useState, useEffect } from "react";
import { fetchContestList } from "../api-client";
import Header from "./Header";

const ContestList = ({ initialContests, onContestClick }) => {
  const [contests, setContests] = useState(
    initialContests ?? [],
  );

  useEffect(() => {
    if (!initialContests) {
      fetchContestList().then((contests) => {
        setContests(contests);
      });
    }
  }, [initialContests]);

  return (
    <>
      <Header message="Naming Contests" />

      <div className="contest-list">
        {contests.map((contest) => {
          return (
            <ContestPreview
              key={contest.id}
              contest={contest}
              onContestClick={onContestClick}
            />
          );
        })}
      </div>
    </>
  );
};

export default ContestList;
