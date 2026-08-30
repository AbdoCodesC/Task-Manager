import { User, Star } from "lucide-react";

function Profile() {
  return (
    <div className="flex flex-col w-full h-screen overflow-hidden p-5">
      {/* Top */}
      <div className="flex justify-between p-10 items-start w-full min-h-0 rounded-md">
        {/* User */}
        <div className="flex w-full justify-around items-center gap-10">
          <div className="flex p-2 bg-blue-200 rounded-full">
            <a href="/settings">
              <User size={70} />
            </a>
          </div>
          <div className="flex flex-col gap-2 w-full justify-center items-start">
            <p className="text-lg font-bold">Abdo Chaibe</p>
            <p className="text-sm">abdeerbusiness@gmail.com</p>
            <p className="text-xs">Software Engineer</p>
          </div>
        </div>
      </div>
      {/* Rate */}
      <div className="flex justify-around w-full min-h-0 p-10 border-b border-gray-300">
        <div className="flex flex-col justify-center items-center">
          <p className="text-xl font-bold">24</p>
          <p className="text-md text-gray-400">Projects</p>
        </div>
        <div className="flex flex-col justify-center items-center">
          <p className="text-xl font-bold">128</p>
          <p className="text-md text-gray-400">Tasks</p>
        </div>
        <div className="flex flex-col justify-center items-center">
          <p className="text-xl font-bold">85%</p>
          <p className="text-md text-gray-400">Completion Rate</p>
        </div>
      </div>
      {/* Bottom */}
      <div className="flex justify-between  min-h-0 h-full p-2 ">
        <div className="flex flex-col justify-start p-10 border-r border-gray-300 w-full flex-1">
          <p className="font-bold text-lg">About</p>
          <p className="text-md mt-5">
            Passionate about creating and building beautiful user experiences
          </p>
        </div>
        <div className="flex flex-col justify-start p-10 w-full flex-1 h-full ">
          <p className="font-bold text-lg">Recent Activity</p>
          <div className="flex flex-col gap-2 mt-5 overflow-scroll">
            <div className="flex gap-2 justify-start items-center">
              <div className="p-1 bg-blue-100 rounded-full">
                <Star size={14} />
              </div>
              <p>Completed 3 tasks today</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
