import axios from "axios";
import type { User, Task } from "../types/index";
import type { LoginResponse } from "../types/index";

const API_URL: string =
  import.meta.env.VITE_API_URL || console.log("url not injected.");

// const api = axios.create({
//   baseURL: API_URL,
// });

// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem("token");
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//     console.log("Token used!!");
//   }
//   return config;
// });

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
        error.response?.data?.error ||
        error ||
        "Login failed, please try again.";
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
}): Promise<LoginResponse | void> {
  try {
    const response = await axios.post<LoginResponse>(
      `${API_URL}/auth/signup`,
      data,
    );
    console.log(response);
    if (response.status === 201) {
      return response.data;
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.error ||
        error ||
        "Signup failed, please try again.";
      throw new Error(message);
    }
    throw new Error("Network error. Please check your connection");
  }
}

// - logout
export async function logout(): Promise<void> {
  try {
    const response = await axios.post(`${API_URL}/auth/logout`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    if (response.status === 200) {
      localStorage.removeItem("token");
      return;
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.error ||
        error ||
        "Signup failed, please try again.";
      throw new Error(message);
    }
    throw new Error("Network error. Please check your connection");
  }
}

// TASKS
export async function getTasks(): Promise<Task[]> {
  try {
    console.log(`${API_URL}/tasks`);
    // return []
    const response = await axios.get(`${API_URL}/tasks`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    const data = await response?.data;
    console.log(response, "  ", data);
    if (data && Array.isArray(data.tasks)) return data.tasks as Task[];
    if (Array.isArray(data)) {
      return data as Task[];
    }
    return [];
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log(error);
      throw new Error(error.message);
    }
    throw new Error("Network error. Please check your connection");
  }
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
  const response = await axios.post<PostTaskResponse>(`${API_URL}/tasks`, data);
  return response.data;
}

// USERS
type PostUserResponse = User & { id: number };
export async function getUser(id: number): Promise<PostUserResponse> {
  const response = await axios.get<PostUserResponse>(`${API_URL}/users/${id}`);
  return response.data;
}
