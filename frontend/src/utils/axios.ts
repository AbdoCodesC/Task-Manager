import axios from "axios";
import type { User, Task } from "../types/index";
import type { LoginResponse } from "../types/index";

const API_URL: string =
  import.meta.env.VITE_API_URL || console.log("url not injected.");

// AUTH
// AUTH
// - login

export async function login(data: {
  email: string;
  password: string;
}): Promise<LoginResponse | Error | void> {
  try {
    const response = await axios.post<LoginResponse>(
      `${API_URL}/auth/login`,
      data,
    );
    console.log(response);
    if (response.status === 200) {
      console.log("returning data here!.");
      return response.data;
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.error || "Login failed, please try again.";
      throw new Error(message);
    }
    throw new Error("Network error. Please check your connection");
  }
}

// - signup

export async function signup(data: {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}): Promise<LoginResponse | Error | void> {
  try {
    const response = await axios.post<LoginResponse>(
      `${API_URL}/auth/signup`,
      data
    );
    console.log(response);
    if (response.status === 201) {
      return response.data;
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.error || "Signup failed, please try again.";
      throw new Error(message);
    }
    throw new Error("Network error. Please check your connection");
  }
}

// - logout

// TASKS
export async function getTasks(): Promise<Task[]> {
  const response = await axios.get(`${API_URL}/tasks`);
  let data = response.data;
  console.log(response, "  ", data);
  return response.data;
}

export async function getTask(id: number): Promise<Task> {
  const response = await axios.get<Task>(`${API_URL}/tasks/${id}`);
  let data = response.data;
  console.log(response, "  ", data);
  return response.data;
}

type PostTaskResponse = Task & { id: number };

export async function addTask(data: Task): Promise<PostTaskResponse> {
  console.log(data);
  const response = await axios.post<PostTaskResponse>(
    `${API_URL}/tasks/`,
    data,
  );
  return response.data;
}

// USERS
type PostUserResponse = User & { id: number };
export async function getUser(id: number): Promise<PostUserResponse> {
  const response = await axios.get<PostUserResponse>(`${API_URL}/users/${id}`);
  return response.data;
}
