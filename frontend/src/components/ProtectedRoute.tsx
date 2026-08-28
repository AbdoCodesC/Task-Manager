import { Outlet, Navigate } from "react-router";

export default function ProtectedRoute() {
  const isAuthenticated = localStorage.getItem("token"); //TODO make this better
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}
