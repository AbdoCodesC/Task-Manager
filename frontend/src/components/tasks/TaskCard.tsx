import type { Task } from "../../types";

export default function TaskCard({ task }: { task: Task }) {
  return (
    <div className="mb-5">
      <p>Task: {task.title}</p>
      <p>Duration: {task.duration}</p>
      <p>Status: {task.status}</p>
      <p>Priority: {task.priority}</p>
    </div>
  );
}
