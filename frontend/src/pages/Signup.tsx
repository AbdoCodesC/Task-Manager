import React, { useState } from "react";
import { useNavigate } from "react-router";
import { signup } from "../utils/axios";
import { info } from "../utils/toast";
import { EyeOff, SquareCheckBig, User, Lock, Mail } from "lucide-react";

interface InvalidInput {
  full_name?: boolean;
  email?: boolean;
  password?: boolean;
  confirm_password?: boolean;
}

function Signup() {
  const navigate = useNavigate();
  const [error, setError] = useState<string>();
  const [hidePass, setHidePass] = useState<boolean>(true);
  const [hideConfirmPass, setHideConfirmPass] = useState<boolean>(true);
  const [invalid, setInvalid] = useState<InvalidInput>({
    full_name: false,
    email: false,
    password: false,
    confirm_password: false,
  });

  async function signupHandler(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const form_data = new FormData(e.currentTarget);
    console.log(form_data);

    const full_name = form_data.get("full_name")?.toString().trim();
    console.log(full_name!.split(" ").length);
    if (!full_name || (full_name && full_name.split(" ").length != 2)) {
      console.error("Add your fullname (eg. john doe)");
      setInvalid((prev) => ({ ...prev, full_name: true }));
    } else setInvalid((prev) => ({ ...prev, full_name: false }));

    const email = form_data.get("email")?.toString().trim();
    if (!email) {
      setInvalid((prev) => ({ ...prev, email: true }));
    } else setInvalid((prev) => ({ ...prev, email: false }));

    const password = form_data.get("password")?.toString().trim();
    if (!password) {
      setInvalid((prev) => ({ ...prev, password: true }));
    } else setInvalid((prev) => ({ ...prev, password: false }));

    const confirm_password = form_data
      .get("confirm_password")
      ?.toString()
      .trim();
    if (!confirm_password) {
      setInvalid((prev) => ({ ...prev, confirm_password: true }));
    } else setInvalid((prev) => ({ ...prev, confirm_password: false }));

    console.log();

    if (!email || !full_name || !password || !confirm_password) return;

    const first_name = full_name!.split(" ")[0];
    const last_name = full_name!.split(" ")[1];

    if (password != confirm_password) {
      setInvalid((prev) => ({
        ...prev,
        confirm_password: true,
        password: true,
      }));

      console.error("Passwords do not match, try again");
      return;
    } else
      setInvalid((prev) => ({
        ...prev,
        confirm_password: false,
        password: false,
      }));

    if (!first_name || !last_name || !email || !password || !confirm_password)
      return;
    try {
      const data = await signup({ first_name, last_name, email, password });
      localStorage.setItem("token", data["access_token"]);
      info(`Welcome, ${full_name}`);
      navigate("/task");
    } catch (error) {
      if (error instanceof Error) setError(error.message);
      else console.log(error);
    }
  }

  console.log(
    "Keys: ",
    Object.keys(invalid),
    " ",
    "Values: ",
    Object.values(invalid),
  );

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

  function handlePass(e: React.MouseEvent) {
    e.preventDefault();
    setHidePass((prev) => !prev);
  }
  function handleConfirmPass(e: React.MouseEvent) {
    e.preventDefault();
    setHideConfirmPass((prev) => !prev);
  }

  return (
    <div className="w-full h-screen overflow-hidden min-h-0 ">
      <div className="flex w-full">
        {/* Left - image */}
        <div className="flex flex-1 items-center justify-center ">
          <img src="/girl.svg" className="object-center h-screen " />
        </div>
        {/* Right */}
        <div className="flex flex-1 h-screen py-10 px-5">
          {/* Login */}
          <div className="flex flex-col justify-around items-start w-full px-10">
            {/* Top */}
            <div className="flex flex-col justify-between items-start flex-1">
              <div className="flex flex-1 gap-3">
                <SquareCheckBig color="#dbeafe" size={30} strokeWidth={3} />
                <h1 className="font-bold text-xl">TaskManager</h1>
              </div>
              <div className="flex flex-col gap-3 items-start flex-1">
                <p className="text-2xl font-bold text-blue-900">
                  Create your account
                </p>
                <p className="text-md text-gray-400">
                  Get started with your free account
                </p>
              </div>
            </div>
            {/* Form */}
            <form
              method="POST"
              onSubmit={signupHandler}
              className="w-full flex flex-col flex-2 justify-around pr-10"
            >
              <div className="relative flex flex-col">
                <label htmlFor="full_name" className="font-bold">
                  Full name
                </label>
                <User
                  size={24}
                  className="absolute top-10 left-2 text-blue-200 "
                />
                <input
                  type="text"
                  name="full_name"
                  placeholder="Enter your full name"
                  className={`my-2 ${invalid && invalid["full_name"] ? "border-red-400" : "border-blue-100"} border-solid border rounded-md px-10 py-2`}
                />
              </div>

              <div className="relative flex flex-col">
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

              <div className="flex flex-col relative">
                <label htmlFor="password" className="font-bold">
                  Password
                </label>

                <Lock
                  size={24}
                  className="absolute top-10 left-2 text-blue-200"
                />
                <input
                  name="password"
                  type={hidePass ? "password" : "text"}
                  placeholder="Create a password"
                  className={`my-2 ${invalid && invalid["password"] ? "border-red-400" : "border-blue-100"} border-solid border rounded-md px-10 py-2`}
                />
                <button className="cursor-pointer" onClick={handlePass}>
                  <EyeOff
                    size={20}
                    className="absolute top-10 right-2 text-blue-200"
                  />
                </button>
              </div>
              <div className="flex flex-col relative">
                <label htmlFor="confirm_password" className="font-bold">
                  Confirm password
                </label>

                <Lock
                  size={24}
                  className="absolute top-10 left-2 text-blue-200"
                />
                <input
                  name="confirm_password"
                  type={hideConfirmPass ? "password" : "text"}
                  placeholder="Confirm your password"
                  className={`my-2 ${invalid && invalid["confirm_password"] ? "border-red-400" : "border-blue-100"} border-solid border rounded-md px-10 py-2`}
                />
                <button className="cursor-pointer" onClick={handleConfirmPass}>
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
                  Signup
                </button>
              </div>
            </form>
            {/* End */}
            <div className="flex py-5">
              <p>
                Already have an account?{" "}
                <a
                  href="/login"
                  className="hover:text-blue-300 cursor-pointer underline mt-2"
                >
                  login
                </a>
              </p>
            </div>
            <div className="flex">{error && errorMessage()}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Signup;
