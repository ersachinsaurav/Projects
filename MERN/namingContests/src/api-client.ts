import axios from "axios";
import { API_SERVER_URL } from "./public-config";

export const fetchContestList = async () => {
  const res = await axios.get(`${API_SERVER_URL}/contests`);
  return res.data.contests;
};

export const fetchContest = async (contestId) => {
  const res = await axios.get(
    `${API_SERVER_URL}/contest/${contestId}`,
  );
  return res.data.contest;
};

export const addNewNameToContest = async ({
  contestId,
  newName,
}) => {
  const res = await axios.post(
    `${API_SERVER_URL}/contest/${contestId}`,
    { newName },
  );
  return res.data.updatedContest;
};

export const addContest = async (contestData) => {
  const res = await axios.post(
    `${API_SERVER_URL}/contests`,
    contestData,
  );
  return res.data.contest;
};
