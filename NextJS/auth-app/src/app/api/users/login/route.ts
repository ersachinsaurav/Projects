import { dbConnection } from "@/dbConfig/dbConfig";
import User from "@/models/usersModel";
import { NextRequest, NextResponse } from "next/server";
import bcryptjs from "bcryptjs";
import jwt from "jsonwebtoken";

dbConnection();

export async function POST(request: NextRequest) {
  try {
    const reqBody = await request.json();
    const { username, password } = reqBody;

    //check if user exists
    let userData = await User.findOne({ username: username });
    if (!userData) {
      return NextResponse.json({ message: "Username not found", status: 400 });
    }

    //verify password
    const validPassword = await bcryptjs.compare(password, userData.password);
    if (!validPassword) {
      return NextResponse.json({ message: "Incorrect password", status: 400 });
    }

    //check email verification status
    if (!userData.isVerified) {
      return NextResponse.json({
        message: "Email verification pending",
        status: 400,
      });
    }

    //create tokenData
    const tokenData = {
      id: userData._id,
      username: userData.username,
      email: userData.email,
    };

    //create token
    const token = await jwt.sign(tokenData, process.env.tokenSecret!, {
      expiresIn: "1d",
    });

    //create response
    const response = NextResponse.json({
      message: "Login successful",
      success: true,
      status: 200,
    });

    //update cookie
    response.cookies.set("token", token, {
      httpOnly: true,
    });

    return response;
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 500 });
  }
}
