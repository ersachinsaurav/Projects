import React from "react";

const ContestPreview: React.FC<{
  contest: object;
  onContestClick: any;
}> = ({ contest, onContestClick }) => {
  const handleClick = (event) => {
    event.preventDefault();
    // Navigate to a new view
    onContestClick(contest.id);
  };

  return (
    <div className="contest-preview link" onClick={handleClick}>
      <div className="category">{contest.categoryName}</div>
      <div className="contest">{contest.contestName}</div>
    </div>
  );
};

export default ContestPreview;
