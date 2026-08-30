import { login } from "../utils/axios";
import React, { useState } from "react";
import { useNavigate } from "react-router";
import { info } from "../utils/toast";
import { EyeOff, Lock, Mail, SquareCheckBig } from "lucide-react";

interface InvalidInput {
  email?: boolean;
  password?: boolean;
}

function Login() {
  const [error, setError] = useState<string>("");
  const [hidePass, setHidePass] = useState<boolean>(true);
  const [invalid, setInvalid] = useState<InvalidInput>({
    email: false,
    password: false,
  });
  const navigate = useNavigate();

  async function loginHandler(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const form_data = new FormData(e.currentTarget);
    const email = form_data.get("email")?.toString();
    if (!email) setInvalid((prev) => ({ ...prev, email: true }));
    else setInvalid((prev) => ({ ...prev, email: false }));

    const password = form_data.get("password")?.toString();
    if (!password) setInvalid((prev) => ({ ...prev, password: true }));
    else setInvalid((prev) => ({ ...prev, password: false }));

    if (!email || !password) return;
    try {
      const data = await login({ email, password });
      if (!data) return;
      localStorage.setItem("token", data["access_token"]);
      info(`Welcome, ${data["user"]?.full_name}`);
      navigate("/task");
    } catch (error) {
      if (error instanceof Error) setError(error.message);
      else console.log(error);
    }
  }

  function handlePass(e: React.MouseEvent) {
    e.preventDefault();
    setHidePass((prev) => !prev);
  }

  function errorMessage() {
    if (error === "AxiosError: Network Error") {
      return (
        <p className="text-red-400 text-sm">
          Connection error, server not responding.
        </p>
      );
    } else {
      return <p className="text-red-400 text-sm">{error}</p>;
    }
  }

  return (
    <div className="w-full h-screen overflow-hidden min-h-0 ">
      <div className="flex w-full">
        {/* Left - image */}
        <div className="flex flex-1 items-center justify-center ">
          <img src="/boy.svg" className="object-center h-screen " />
        </div>
        {/* Right */}
        <div className="flex flex-1 h-screen py-10 px-5">
          {/* Login */}
          <div className="flex flex-col justify-around items-start w-full px-10">
            {/* Top */}
            <div className="flex flex-col items-start w-full flex-1">
              <div className="flex gap-3 flex-1">
                <SquareCheckBig color="#dbeafe" size={30} strokeWidth={3} />
                <h1 className="font-bold text-xl">TaskManager</h1>
              </div>
              <div className="flex flex-col gap-3 items-start flex-1">
                <p className="text-2xl font-bold text-blue-900">
                  Welcome back!
                </p>
                <p className="text-md text-gray-400">
                  Login to continue to your account
                </p>
              </div>
            </div>
            {/* Form */}
            <form
              method="POST"
              onSubmit={loginHandler}
              className="w-full flex flex-col gap-10 mt-10 pr-10 mb-0 flex-2"
            >
              <div className="relative flex flex-col ">
                <label htmlFor="email" className="font-bold">
                  Email
                </label>
                <Mail
                  size={24}
                  className="absolute top-10 left-2 text-blue-200 "
                />
                <input
                  type="text"
                  name="email"
                  placeholder="Enter your email"
                  className={`my-2 ${invalid && invalid["email"] ? "border-red-400" : "border-blue-100"} border-solid border rounded-md px-10 py-2`}
                />
              </div>

              <div className="flex flex-col relative ">
                <div className="flex justify-between items-center">
                  <label htmlFor="password" className="font-bold">
                    Password
                  </label>
                  <p className="text-sm text-blue-200 hover:underline cursor-pointer">
                    Forgot password?
                  </p>
                </div>

                <Lock
                  size={24}
                  className="absolute top-10 left-2 text-blue-200"
                />
                <input
                  name="password"
                  type={hidePass ? "password" : "text"}
                  placeholder="Enter your password"
                  className={`my-2 ${invalid && invalid["password"] ? "border-red-400" : "border-blue-100"} border-solid border rounded-md px-10 py-2`}
                />
                <button className="cursor-pointer" onClick={handlePass}>
                  <EyeOff
                    size={20}
                    className="absolute top-10 right-2 text-blue-200"
                  />
                </button>
              </div>
              <div className="flex flex-col">
                <button
                  type="submit"
                  className="p-2 bg-blue-100 rounded-sm cursor-pointer text-gray-500 hover:bg-blue-300"
                >
                  Login
                </button>
                {/* End */}
                <div className="flex mt-5">
                  <p>
                    Don't have an account?{" "}
                    <a
                      href="/signup"
                      className="hover:text-blue-300 cursor-pointer underline mt-2"
                    >
                      signup
                    </a>
                  </p>
                </div>
              </div>
            </form>
            <div className="flex justify-center w-full h-7">
              <p hidden={error ? false : true}>{error && errorMessage()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
