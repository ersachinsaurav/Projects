"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";

export default function loginPage() {
  const router = useRouter();
  const [user, setUser] = useState({
    password: "",
    username: "",
  });

  const [buttonDisabled, setButtonDisabled] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user.username.length > 0 && user.password.length > 0) {
      setButtonDisabled(false);
    } else {
      setButtonDisabled(true);
    }
  }, [user]);

  const handleLogin = async () => {
    try {
      setLoading(true);
      const response = await axios.post("api/users/login", user);

      if (response.data.status == 400) {
        toast.error(response.data.message, {
          duration: 3000,
          position: "top-center",
        });
        return;
      }

      router.push("/dashboard");
    } catch (error: any) {
      console.error(error.message);
      toast.error(error.message, {
        duration: 3000,
        position: "top-center",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="mb-4">{loading ? "Processing" : "Login"}</h1>
      <hr />
      <label htmlFor="username">Username: </label>
      <input
        type="text"
        name="username"
        id="username"
        className="p-2 border-gray-300 focus:border-gray-600 mb-4"
        placeholder="Username"
        onChange={(e) => setUser({ ...user, username: e.target.value })}
      />
      <label htmlFor="password">Password: </label>
      <input
        type="password"
        name="password"
        id="password"
        className="p-2 border-gray-300 focus:border-gray-600 mb-4"
        placeholder="Password"
        onChange={(e) => setUser({ ...user, password: e.target.value })}
      />

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleLogin}
        disabled={buttonDisabled}
      >
        Continue
      </button>
      <Link href={"/signup"}>Don't have an account? Sign Up</Link>
      <Toaster position="top-center" reverseOrder={false} />
    </div>
  );
}
