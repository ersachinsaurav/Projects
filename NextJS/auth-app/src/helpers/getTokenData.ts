import { NextRequest, NextResponse } from "next/server";
import jwt from "jsonwebtoken";

export const getTokenData = (request: NextRequest) => {
  try {
    const token = request.cookies.get("token")?.value || "";
    const decodedToken: any = jwt.verify(token, process.env.tokenSecret!);
    return decodedToken.id;
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 400 });
  }
};
