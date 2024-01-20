import { NextResponse } from "next/server";

export async function GET() {
  try {
    const response = NextResponse.json({
      message: "Logout successfully",
      success: true,
      status: 200,
    });

    response.cookies.set("token", "", {
      expires: new Date(0),
    });

    return response;
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 500 });
  }
}
