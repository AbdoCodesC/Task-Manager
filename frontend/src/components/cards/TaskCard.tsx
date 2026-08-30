import { Calendar, EllipsisVertical, User } from "lucide-react";

function TaskCard({
  title,
  project,
  priority,
  status,
  date,
  // userImage,
}: {
  title?: string;
  project?: string;
  priority: "High" | "Medium" | "Low";
  status?: "In Progress" | "Pending" | "Completed";
  date?: string;
  // userImage: string | undefined | never;
}) {
  return (
    <div className="flex justify-between items-center h-20 shrink-0 shadow-sm rounded-md p-5 bg-white">
      {/* Card Itself */}
      {/* Left */}
      <div className="flex justify-start items-center gap-10 flex-1">
        <input
          type="checkbox"
          className="w-5 h-5 has-checked:bg-blue-100 cursor-pointer "
        />
        <div className="flex flex-col justify-between items-start">
          <p className="text-lg py-1">{title}</p>
          <div className="flex py-1 px-2 items-center justify-center text-blue-400 bg-blue-100 rounded-md">
            <p className="text-sm">{project}</p>
          </div>
        </div>
      </div>
      {/* Right */}
      <div className="flex justify-end items-center p-1 flex-1 ">
        <div className="flex flex-1  justify-start">
          <div
            className={`p-1 ${priority === "High" ? "bg-red-100 text-red-400" : priority === "Medium" ? "bg-orange-100 text-orange-400" : "bg-yellow-100 text-yellow-400"} rounded-md text-xs font-semibold`}
          >
            {priority}
          </div>
        </div>
        <div className="flex flex-1">
          <div
            className={`p-1 ${status === "In Progress" ? "bg-orange-100 text-orange-400" : status === "Pending" ? "bg-gray-100 text-gray-400" : "bg-green-100 text-green-400"} rounded-md text-xs font-semibold`}
          >
            {status}
          </div>
        </div>
        <div className="flex flex-1">
          <div className="flex  justify-center items-center text-xs gap-1 text-gray-500">
            <Calendar size={14} />
            <p>{date}</p>
          </div>
        </div>
        <div className="flex flex-1">
          <div className="flex justify-center items-center rounded-full p-1 bg-blue-100">
            <User size={30} className="cursor-pointer" />
            {/* {userImage} - will add later */}
          </div>
        </div>
        {/* <div className="flex flex-1"> */}
        <button className="cursor-pointer">
          <EllipsisVertical />
        </button>
        {/* </div> */}
      </div>
    </div>
  );
}

export default TaskCard;
