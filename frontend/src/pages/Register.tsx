import React from "react";
import { useNavigate } from "react-router";
import { signup } from "../utils/axios";

function Register() {
  const navigate = useNavigate();
  async function registerHandler(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form_data = new FormData(e.currentTarget);
    const first_name = form_data.get("first_name")?.toString().trim();
    const last_name = form_data.get("last_name")?.toString().trim();
    const email = form_data.get("email")?.toString().trim();
    const password = form_data.get("password")?.toString().trim();
    if (!first_name || !last_name || !email || !password) return;
    try {
      const data = await signup({ first_name, last_name, email, password });
      console.log(data);
      localStorage.setItem("cookie", data["access_token"]);
      navigate("/home");
    } catch (error) {
      console.log(error);
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
            onSubmit={(e: React.FormEvent<HTMLFormElement>) =>
              registerHandler(e)
            }
            className="w-full"
          >
            <div className="mb-4 flex flex-col">
              <label htmlFor="first_name">First name</label>
              <input
                type="text"
                name="first_name"
                placeholder="john"
                required
                className="my-2 border-blue-100 border-solid border rounded-md p-2"
              />
            </div>
            <div className="mb-4 flex flex-col">
              <label htmlFor="first_name">Last name</label>
              <input
                type="text"
                name="last_name"
                placeholder="doe"
                required
                className="my-2 border-blue-100 border-solid border rounded-md p-2"
              />
            </div>
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
                Sign up
              </button>
            </div>
            <button onClick={() => navigate("/login")}>
              <span className="hover:text-blue-300 cursor-pointer underline">
                login
              </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
