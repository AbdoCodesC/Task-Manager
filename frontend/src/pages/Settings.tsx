import { User } from "lucide-react";

function Settings() {
  return (
    <div className="w-full flex h-screen overflow-hidden">
      <div className="flex justify-between w-full border ">
        {/* Left */}
        <div className="flex flex-col gap-25 items-start flex-1 w-full p-5">
          <div className="flex">
            <p className="font-bold text-lg">Profile Settings</p>
          </div>

          <div className="flex flex-col gap-2 w-full">
            <p className="text-lg text-gray-500">Full Name</p>
            <input
              type="text"
              value="Abdo Chaibe"
              className="border border-gray-200 py-2 px-2 w-full rounded-md"
            />
          </div>
          <div className="flex flex-col gap-2 w-full">
            <p className="text-lg text-gray-500">Email</p>
            <input
              type="text"
              value="abdeerbusiness@gmail.com"
              className="border border-gray-200 py-2 px-2 w-full rounded-md"
            />
          </div>
          <div className="flex flex-col gap-2 w-full">
            <p className="text-lg text-gray-500">Bio</p>
            <textarea
              value="Passionate about creating great products"
              className="border border-gray-200 py-2 px-2 w-full rounded-md"
            />
          </div>
          {/* button */}
          <button className="py-2 px-3 bg-blue-600 text-white hover:bg-blue-500 cursor-pointer rounded-md">
            Save Changes
          </button>
        </div>
        {/* Right */}
        <div className="flex justify-center items-center flex-1">
          <div className="flex flex-col gap-5 items-center justify-center p-10 shadow-md rounded-md">
            <div className="p-20 bg-gray-200 rounded-full shadow-sm">
              <User size={100} />
            </div>
            <button className="py-2 px-3 bg-black text-white flex justify-center items-center rounded-md  hover:bg-gray-800 cursor-pointer">
              Change Photo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
