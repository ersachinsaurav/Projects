import express from "express";
import cors from "cors";
import { connectClient } from "./db";

const apiRouter = express.Router();
apiRouter.use(cors());
apiRouter.use(express.json());

apiRouter.get("/contests", async (req, res) => {
  const client = await connectClient();

  const contests = await client
    .collection("contests")
    .find()
    .project({ _id: 0, id: 1, categoryName: 1, contestName: 1 })
    .toArray();

  res.send({ contests });
});

apiRouter.get("/contest/:contestId", async (req, res) => {
  const client = await connectClient();
  const contest = await client
    .collection("contests")
    .findOne({ id: req.params.contestId });

  res.send({ contest });
});

apiRouter.post("/contest/:contestId", async (req, res) => {
  const client = await connectClient();

  const { newName } = req.body;

  const contestDoc = await client
    .collection("contests")
    .findOneAndUpdate(
      { id: req.params.contestId },
      {
        $push: {
          names: {
            id: newName.toLowerCase().replace(/\s/g, "-"),
            name: newName,
            timestamp: new Date(),
          },
        },
      },
      { returnDocument: "after" },
    );

  res.send({ updatedContest: contestDoc.value });
});

apiRouter.post("/contests", async (req, res) => {
  const { contestName, categoryName, description } = req.body;

  const client = await connectClient();
  const newContestDoc = await client
    .collection("contests")
    .insertOne({
      id: contestName.toLowerCase().replace(/\s/g, "-"),
      contestName,
      categoryName,
      description,
      names: [],
    });

  const contest = await client
    .collection("contests")
    .findOne({ _id: newContestDoc.insertedId });

  res.send({ contest });
});

export default apiRouter;
