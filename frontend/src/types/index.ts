export interface User {
  firstName: string,
  lastName: string,
  email: string,
  password: string
}

export interface Task {
  title: string,
  priority?: "low" | "medium" | "high",
  status?: "pending" | "in_progress" | "completed",
  start_time?: Date,
  end_time?: Date,
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

// export type 