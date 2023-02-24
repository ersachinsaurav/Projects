require("dotenv").config();
const env = process.env;
export const PORT = env.PORT ?? "777";
export const HOST = env.HOST ?? "127.0.0.1";
export const SERVER_URL = `http://${HOST}:${PORT}`;
export const MONGO_DB_URI =
  env.MONGO_DB_URI ?? "mongodb://127.0.0.1:27017";
export const DBNAME = env.DBNAME ?? "local";

export default {
  PORT,
  HOST,
  SERVER_URL,
  MONGO_DB_URI,
  DBNAME,
};
