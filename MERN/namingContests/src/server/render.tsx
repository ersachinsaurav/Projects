import ReactDOMServer from "react-dom/server";
import { fetchContestList, fetchContest } from "../api-client";
import App from "../components/App";

const serverRender = async (req) => {
  const { contestId } = req.params;

  const initialData = contestId
    ? { currentContest: await fetchContest(contestId) }
    : { contests: await fetchContestList() };

  const initialMarkup = ReactDOMServer.renderToString(
    <App initialData={initialData} />,
  );

  return { initialMarkup, initialData };
};

export default serverRender;
