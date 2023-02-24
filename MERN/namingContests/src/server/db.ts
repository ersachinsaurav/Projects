import { MongoClient } from "mongodb";
import config from "./config";

let connectedClient;

export const connectClient = async () => {
  if (connectedClient) {
    return connectedClient.db(config.DBNAME);
  }

  const client = new MongoClient(config.MONGO_DB_URI);
  await client.connect();
  connectedClient = client;
  return connectedClient.db(config.DBNAME);
};

export const stopClient = async () => {
  await connectedClient?.close();
};
