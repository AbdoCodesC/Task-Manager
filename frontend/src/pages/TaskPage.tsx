import { Bell, ChartNoAxesCombined, Search, User } from "lucide-react";

import {
  HomeIcon,
  SquareCheckBig,
  EyeClosed,
  ListTodo,
  CalendarDays,
  CalendarClock,
  Funnel,
  Plus,
} from "lucide-react";
import SideBarCard from "../components/cards/SideBarCard";
import ProjectCard from "../components/cards/ProjectCard";
import Tasks from "../components/tasks/Tasks";
import { useState } from "react";
import {useDebounce} from '@uidotdev/usehooks'

function TaskPage() {
  const [view, setView] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const debouncedSearchTerm = useDebounce(search, 300) // to optimize search
  // const [tasks, setTasks] = useState<Task[]>([]);

  // const [showTasks, setShowTasks] = useState<boolean>(true);

  // useEffect(() => {
  //   async function get_tasks(): Promise<void> {
  //     const data = await getTasks();
  //     console.log("data--> ", data);
  //     if (!data) return;
  //     setTasks(data);
  //   }
  //   get_tasks();
  // }, []);

  function handleSearch(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    if (view !== "tasks") {
      setSearch("");
      return;
    }
    setSearch(e.currentTarget.value);
  }

  function handleView(component: string): void {
    setView(component);
  }

  return (
    <div className="h-dvh w-full overflow-hidden flex box-border">
      {/* Side Bar */}
      <div className="flex flex-col w-80 h-full min-h-0 border-r border-gray-300 p-5">
        {/* First */}
        <div className="flex flex-col justify-start w-full mb-10">
          <div className="flex flex-row justify-between">
            <div className="flex">
              <SquareCheckBig color="#dbeafe" size={30} />
              <h1 className="ml-1 font-bold text-xl">TaskManager</h1>
            </div>
            <div className="flex">
              <EyeClosed size={30} />
            </div>
          </div>
        </div>

        {/* Middle - Main contents */}
        <div className="flex flex-col items-start justify-start gap-2 w-full mb-10">
          <a href="/" className="w-full">
            <SideBarCard
              Icon={HomeIcon}
              title="Dashboard"
              handleView={handleView}
            />
          </a>
          <SideBarCard Icon={ListTodo} title="Tasks" handleView={handleView} />
          <SideBarCard
            Icon={CalendarDays}
            title="Today"
            handleView={handleView}
          />
          <SideBarCard
            Icon={CalendarClock}
            title="Upcoming"
            handleView={handleView}
          />
          <SideBarCard Icon={Funnel} title="Filters" handleView={handleView} />
          <SideBarCard
            Icon={ChartNoAxesCombined}
            title="Analytics"
            handleView={handleView}
          />
        </div>

        {/* Projects */}
        <div className="flex flex-col gap-5 w-full flex-1 min-h-0">
          <div className="flex  justify-between items-center text-gray-400 mb-1">
            <p>PROJECTS</p>
            <a href="/create-project">
              <Plus size={20} /> {/* DO MODAL HERE */}
            </a>
          </div>
          {/* Projects - CUSTOM data - project[] later  */}
          <div className="flex flex-col w-full gap-2 overflow-y-auto scrollbar-thumb-gray-200">
            <ProjectCard bgColor="bg-blue-400" title="Website Redesign" />
            <ProjectCard bgColor="bg-red-400" title="Personal" />
            <ProjectCard bgColor="bg-green-400" title="Mobile App" />
          </div>
        </div>
      </div>

      {/* Tasks & Nav */}
      <div className="flex-1 min-w-0 min-h-0 bg-white flex flex-col">
        {/* Nav */}
        <div className="flex justify-end border-b border-gray-300">
          <div className="flex justify-end gap-5 items-center shrink-0 px-3 py-5">
            <Search className="relative -right-13 text-gray-500" />
            <input
              type="text"
              className="py-2 pr-5 pl-10 border border-gray-200 rounded-md"
              placeholder="Search tasks ..."
              value={search}
              onChange={handleSearch}
            />
            <Bell size={24} className="cursor-pointer" />
            <a href="/profile">
              <div className="flex justify-center items-center rounded-full p-1 bg-blue-100">
                <User size={30} className="cursor-pointer" />
              </div>
            </a>
          </div>
        </div>
        {/* Tasks */}
        {view === "tasks" && <Tasks search={debouncedSearchTerm} />}
        {/* whateveer else */}
      </div>
    </div>
  );
}

export default TaskPage;
