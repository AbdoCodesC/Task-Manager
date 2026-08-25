import axios from "axios";
import { login } from "../utils/axios";
import React, { useState } from "react";
import { useNavigate } from "react-router";

function Login() {
  const [error, setError] = useState<string>("");
  const navigate = useNavigate();

  async function loginHandler(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form_data = new FormData(e.currentTarget);
    const email = form_data.get("email")?.toString();
    const password = form_data.get("password")?.toString();
    if (!email || !password) return;
    try {
      const data = await login({ email, password });
      console.log("data in loginHa", data["access_token"]);
      if (!data) return;
      console.log(data);
      localStorage.setItem("cookie", data["access_token"]);
      console.log("Welcome User ", data["user"]?.full_name);
      navigate("/home");
      return JSON.stringify({ message: data.message, status: 200 });
    } catch (error) {
      if (typeof error === "string") setError(error);
      else console.log(error);
    }
  }

  return (
    <div className="flex flex-col justify-center min-h-screen bg-gray-50">
      <div className="font-bold text-2xl mb-8 self-center">
        Welcome to the <u>one and only</u> "TASK MANAGER"
      </div>
      <div className="flex flex-col border-solid self-center border-gray-100 border w-[50%] p-10 items-center rounded-xl">
        <div className="flex justify-center w-full max-w-md px-4">
          <form
            method="POST"
            onSubmit={(e: React.FormEvent<HTMLFormElement>) => loginHandler(e)}
            className="w-full"
          >
            <div className="mb-4 flex flex-col">
              <label htmlFor="email">Email</label>
              <input
                type="text"
                name="email"
                placeholder="johndoe@gmail.com"
                required
                className="my-2 border-blue-100 border-solid border rounded-md p-2"
              />
            </div>
            <div className="mb-4 flex flex-col">
              <label htmlFor="password">Password</label>
              <input
                name="password"
                type="text"
                placeholder="**********"
                required
                className="my-2 border-blue-100 border-solid border rounded-md p-2"
              />
            </div>
            <div className="mb-1 flex flex-col">
              <button
                type="submit"
                className="p-2 bg-blue-100 rounded-sm cursor-pointer text-gray-500 hover:bg-blue-300"
              >
                Login
              </button>
            </div>
            <button onClick={() => navigate('/register')}>
              <span className="hover:text-blue-300 cursor-pointer underline">signup</span>
            </button>
          </form>
          {error && <p>{error}</p>}
        </div>
      </div>
    </div>
  );
}

export default Login;
