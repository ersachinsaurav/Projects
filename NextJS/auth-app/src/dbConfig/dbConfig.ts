import mongoose from "mongoose";

export async function dbConnection() {
  try {
    mongoose.connect(process.env.mongoURL!);

    const connection = mongoose.connection;

    connection.on("connected", () => {
      console.log("Connection established!");
    });

    connection.on("error", (error) => {
      console.error("MongoDB connection error:", error);
      process.exit(1); // Exit with a non-zero code to indicate failure
    });
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
    process.exit(1); // Exit with a non-zero code to indicate failure
  }
}
