import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import Login from "./pages/Login.tsx";
import Home from "./pages/Home.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import TaskPage from "./pages/TaskPage.tsx";
import ProtectedRoute from "./components/ProtectedRoute.tsx";
import "react-toastify/ReactToastify.css";
import { ToastContainer } from "react-toastify";
import Signup from "./pages/Signup.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <ToastContainer />
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/task" element={<TaskPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
