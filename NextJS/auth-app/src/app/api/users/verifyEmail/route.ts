import { dbConnection } from "@/dbConfig/dbConfig";
import { NextRequest, NextResponse } from "next/server";
import Users from "@/models/usersModel";

dbConnection();

export async function POST(request: NextRequest) {
  try {
    const reqBody = await request.json();
    const { token } = reqBody;

    const userData: any = await Users.findOne({
      verifyToken: token,
      verifyTokenExpiry: { $gt: Date.now() },
    });

    if (!userData) {
      return NextResponse.json({ message: "Invalid token", status: 400 });
    }

    userData.isVerified = true;
    userData.verifyToken = undefined;
    userData.verifyTokenExpiry = undefined;

    await userData.save();

    return NextResponse.json({
      message: "Email verified successfully",
      status: 200,
    });
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 500 });
  }
}
