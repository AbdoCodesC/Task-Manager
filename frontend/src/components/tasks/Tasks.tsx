import TaskCard from "../cards/TaskCard";
import { LayoutGrid, List, Plus } from "lucide-react";
import StatusCard from "../cards/StatusCard";
import { useEffect, useState } from "react";
import type { Task } from "../../types";

function Tasks({ search }: { search: string }) {
  const [filter, setFilter] = useState<string>("all");
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: 1,
      title: "Design Landing Page",
      project: "Website Redesign",
      priority: "high",
      status: "in_progress",
      date: "May 24",
      userImg: "data.png",
    },
    {
      id: 2,
      title: "Go to the gym",
      project: "Lifestyle",
      priority: "medium",
      status: "pending",
      date: "May 25",
      userImg: "data.png",
    },
    {
      id: 3,
      title: "Text friends",
      project: "Personal",
      priority: "low",
      status: "completed",
      date: "May 26",
      userImg: "data.png",
    },
  ]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>();

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

  useEffect(() => {
    filterTasks();
    if (search.length > 0) {
      setFilteredTasks(
        tasks.filter((task) =>
          task.title.toLowerCase().includes(search.toLowerCase()),
        ),
      );
    }
  }, [filter, search]);

  function filterTasks() {
    switch (filter) {
      case "all":
        setFilteredTasks(tasks);
        break;
      case "to do":
        setFilteredTasks(tasks.filter((task) => task.status === "pending"));
        break;
      case "done":
        setFilteredTasks(tasks.filter((task) => task.status === "completed"));
        break;
      case "in progress":
        setFilteredTasks(tasks.filter((task) => task.status === "in_progress"));
        break;
      default:
        return [];
    }
  }

  function handleFilter(filter: string) {
    if (search) {
      setFilter("all");
      return;
    }

    setFilter(filter);
  }

  return (
    <div className="flex flex-col flex-1 min-h-0 w-full px-5 bg-gray-100">
      <div className="flex justify-between items-center h-20">
        <p className="font-bold text-lg">My Tasks</p>
        <button className="flex justify-center items-center text-white py-2 px-5 gap-4 bg-blue-500 cursor-pointer rounded-md hover:bg-blue-400">
          <Plus size={20} />
          New Task
        </button>
      </div>
      {/* config */}
      <div className="flex justify-between w-full">
        <div className="flex gap-10 text-gray-500">
          <StatusCard title="All" handleFilter={handleFilter} filter={filter} />
          <StatusCard
            title="To Do"
            handleFilter={handleFilter}
            filter={filter}
          />
          <StatusCard
            title="In Progress"
            handleFilter={handleFilter}
            filter={filter}
          />
          <StatusCard
            title="Done"
            handleFilter={handleFilter}
            filter={filter}
          />
        </div>
        <div className="flex justify-center items-center">
          <button className="cursor-pointer">
            <div className="p-1 bg-white text-gray-500 rounded-l-md border hover:bg-blue-100">
              <List size={20} />
            </div>
          </button>

          <button className="cursor-pointer">
            <div className="p-1 bg-white text-gray-500 rounded-r-md border hover:bg-blue-100">
              <LayoutGrid size={20} />
            </div>
          </button>
        </div>
      </div>
      {/* actual tasks */}
      <div className="flex flex-col flex-1 min-h-0 gap-4 mt-10 overflow-y-auto last:pb-5 scrollbar-thumb-gray-200 scroll-ml-1">
        {filteredTasks &&
          filteredTasks.map((task) => (
            <TaskCard
              key={task.id}
              title={task.title}
              project={task.project}
              priority={
                task.priority === "high"
                  ? "High"
                  : task.priority === "low"
                    ? "Low"
                    : "Medium"
              }
              status={
                task.status === "completed"
                  ? "Completed"
                  : task.status === "in_progress"
                    ? "In Progress"
                    : "Pending"
              }
              date={task.date}
            />
          ))}
      </div>
    </div>
  );
}

export default Tasks;
