"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function dashboardPage() {
  const router = useRouter();
  const [userId, setUserId] = useState("");

  const getUserData = async () => {
    const response = await axios.get("/api/users/me");
    setUserId(response.data.userData._id);
  };

  useEffect(() => {
    getUserData();
  }, [userId]);

  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    try {
      setLoading(true);
      const response = await axios.get("api/users/logout");

      if (response.data.status == 200) {
        toast.success(response.data.message, {
          duration: 2000,
          position: "top-center",
        });
        router.push("/login");
        return;
      }

      toast.error(response.data.message, {
        duration: 2000,
        position: "top-center",
      });
    } catch (error: any) {
      console.error(error.message);
      toast.error(error.message, {
        duration: 2000,
        position: "top-center",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="mb-4">Dashboard</h1>
      <hr />
      <h2>
        {userId ? (
          <Link
            href={`/dashboard/${userId}`}
            className=" block mx-auto rounded-lg p-3 bg-white ring-2 ring-slate-900/5 shadow-lg space-y-3 hover:bg-sky-500 hover:ring-sky-500"
          >
            Profile Page
          </Link>
        ) : (
          "Fetching user!"
        )}
      </h2>
      <br />
      <button
        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleLogout}
      >
        {loading ? "Processing" : "Logout"}
      </button>
      <Toaster position="top-center" reverseOrder={false} />
    </div>
  );
}
