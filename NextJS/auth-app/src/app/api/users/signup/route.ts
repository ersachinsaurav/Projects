import { dbConnection } from "@/dbConfig/dbConfig";
import Users from "@/models/usersModel";
import { NextRequest, NextResponse } from "next/server";
import bcryptjs from "bcryptjs";
import { sendEmail } from "@/helpers/mailer";

dbConnection();

export async function POST(request: NextRequest) {
  try {
    const reqBody = await request.json();
    const { username, email, password } = reqBody;

    //check if user exists
    let existingUser = await Users.findOne({ username: username });
    if (existingUser) {
      return NextResponse.json({
        message: "Username already exists",
        status: 400,
      });
    }

    existingUser = await Users.findOne({ email: email });
    if (existingUser) {
      return NextResponse.json({
        message: "Email already exists",
        status: 400,
      });
    }

    //hash password
    const salt = await bcryptjs.genSalt(10);
    const hashedPassword = await bcryptjs.hash(password, salt);

    let newUser = new Users({
      username,
      email,
      password: hashedPassword,
    });

    newUser = await newUser.save();

    //send verification email
    await sendEmail({
      email: newUser.email,
      emailType: "VERIFY",
      userId: newUser._id,
    });

    return NextResponse.json({
      message: "User registered successfully",
      newUser,
      status: 200,
    });
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 500 });
  }
}
