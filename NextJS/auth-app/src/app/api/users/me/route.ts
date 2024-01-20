import { getTokenData } from "@/helpers/getTokenData";
import { NextRequest, NextResponse } from "next/server";
import Users from "@/models/usersModel";
import { dbConnection } from "@/dbConfig/dbConfig";

dbConnection();

export async function GET(request: NextRequest) {
  try {
    const userId = await getTokenData(request);
    const userData = await Users.findOne({ _id: userId }).select("-password");
    return NextResponse.json({
      message: "User data available",
      status: 200,
      userData,
    });
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 400 });
  }
}
