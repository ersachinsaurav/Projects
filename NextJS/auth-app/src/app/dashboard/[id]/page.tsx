import React from "react";
import Link from "next/link";
export default function userProfile({ params }: any) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="mb-4">User Profile</h1>
      <hr />
      <p className="text-4xl">Here's my ID : {params.id}</p>
      <br />
      <Link
        href={`/dashboard`}
        className=" block mx-auto rounded-lg p-3 bg-white ring-2 ring-slate-900/5 shadow-lg space-y-3 hover:bg-sky-500 hover:ring-sky-500"
      >
        Dashboard
      </Link>
    </div>
  );
}
