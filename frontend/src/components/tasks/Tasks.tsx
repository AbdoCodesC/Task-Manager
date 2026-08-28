import React, { useEffect, useState } from "react";
import type { Task } from "../../types";
import TaskCard from "./TaskCard";
import { getTasks } from "../../utils/axios";

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);

  const [showTasks, setShowTasks] = useState<boolean>(true);

  useEffect(() => {
    async function get_tasks(): Promise<void> {
      const data = await getTasks();
      console.log("data--> ", data);
      if (!data) return;
      setTasks(data);
    }
    get_tasks();
  }, []);

  return (
    <div className="mt-4 ml-2 border h-full">
      <div className="mb=2">
        <h4>
          All tasks{" "}
          <button
            className="cursor-pointer"
            onClick={() => setShowTasks(!showTasks)}
          >
            &gt;
          </button>
        </h4>
      </div>
      <div className="flex flex-col">
        {showTasks &&
          tasks.map((task) => <TaskCard key={task.id} task={task} />)}
      </div>
    </div>
  );
}

export default Tasks;
