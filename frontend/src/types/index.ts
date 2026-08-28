export interface User {
  firstName: string,
  lastName: string,
  email: string,
  password: string
}

export interface Task {
  id: number,
  title: string,
  priority?: "low" | "medium" | "high",
  status?: "pending" | "in_progress" | "completed",
  start_time?: Date,
  end_time?: Date,
  duration?: number
}

// AUTH
export interface LoginResponse {
  access_cookie: string,
  message: string
  refresh_token: string,
  user: {
    email: string,
    fullName: string,
    id: number,
    role: "user" | "admin" | "moderator",
    tasks?: string[]
  }
};

// Lucid
export interface LucideProps {
  size?: number,
  color?: string,
  strokeWidth?: number
}