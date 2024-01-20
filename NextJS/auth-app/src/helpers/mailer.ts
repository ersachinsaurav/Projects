import nodemailer from "nodemailer";
import Users from "@/models/usersModel";
import bcryptjs from "bcryptjs";
import { NextResponse } from "next/server";

export const sendEmail = async ({ email, emailType, userId }: any) => {
  try {
    //create a hashed token
    const hashedToken = await bcryptjs.hash(userId.toString(), 10);

    if (emailType == "VERIFY") {
      await Users.findByIdAndUpdate(userId, {
        verifyToken: hashedToken,
        verifyTokenExpiry: Date.now() + 3600000,
      });
    } else if (emailType == "RESET") {
      await Users.findByIdAndUpdate(userId, {
        forgotPasswordToken: hashedToken,
        forgotPasswordTokenExpiry: Date.now() + 3600000,
      });
    }

    var transport = nodemailer.createTransport({
      host: "sandbox.smtp.mailtrap.io",
      port: 2525,
      auth: {
        user: process.env.nodemailerUser,
        pass: process.env.nodemailerPass,
      },
    });

    const mailOptions = {
      from: "admin@authapp.co",
      to: email,
      subject:
        emailType === "VERIFY" ? "Verify your email" : "Reset your password",
      html: `<p>Click <a href="${
        process.env.serverURL
      }/verifyEmail?token=${hashedToken}">here</a> to ${
        emailType === "VERIFY" ? "verify your email." : "reset your password."
      }</p>`,
    };

    const mailResponse = await transport.sendMail(mailOptions);
    return mailResponse;
  } catch (error: any) {
    return NextResponse.json({ message: error.message, status: 400 });
  }
};
