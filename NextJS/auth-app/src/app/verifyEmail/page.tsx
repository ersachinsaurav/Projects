"use client";

import axios from "axios";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";

export default function verifyEmailPage() {
  const [token, setToken] = useState("");
  const [verified, setVerified] = useState(false);
  const [error, setError] = useState(false);

  const verifyEmail = async () => {
    try {
      const response = await axios.post("/api/users/verifyEmail", { token });
      if (response.data.status === 200) {
        setVerified(true);
        toast.success(response.data.message, {
          duration: 2000,
          position: "top-center",
        });
      } else {
        setError(true);
        toast.error(response.data.message, {
          duration: 2000,
          position: "top-center",
        });
      }
    } catch (error: any) {
      toast.error(error.message, {
        duration: 2000,
        position: "top-center",
      });
    }
  };

  useEffect(() => {
    const urlToken = window.location.search.split("=")[1];
    setToken(urlToken || "");
  }, []);

  useEffect(() => {
    if (token.length > 0) {
      verifyEmail();
    }
  }, [token]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl">Email Verification Page</h1>
      <br />
      {token ? "" : "No token found"}
      <br />

      {verified && (
        <div>
          <h2 className="text-2xl">Email verified</h2>
          <br />
          <Link href={"/login"} className="text-blue-500">
            Login
          </Link>
        </div>
      )}

      {error && (
        <div>
          <h2 className="text-2xl bg-red">
            Email verification failed. Try again!
          </h2>
        </div>
      )}

      <Toaster position="top-center" reverseOrder={false} />
    </div>
  );
}
