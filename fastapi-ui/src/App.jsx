import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/layout/Sidebar";
import Navbar from "./components/layout/Navbar";
import PageWrapper from "./components/layout/PageWrapper";

import Login from "./pages/auth/Login";
import Dashboard from "./pages/Dashboard";
import UsersList from "./pages/users/UsersList";
import ItemsList from "./pages/items/ItemsList";
import FilesList from "./pages/files/FilesList";
import Health from "./pages/health/Health";
import ResetPassword from "./pages/auth/ResetPassword";

const Private = ({ children }) =>
  localStorage.getItem("access_token") ? children : <Navigate to="/login" />;

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route
          path="/*"
          element={
            <Private>
              <div className="flex">
                <Sidebar />
                <div className="flex-1">
                  <Navbar />
                  <PageWrapper>
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/users" element={<UsersList />} />
                      <Route path="/items" element={<ItemsList />} />
                      <Route path="/files" element={<FilesList />} />
                      <Route path="/health" element={<Health />} />
                    </Routes>
                  </PageWrapper>
                </div>
              </div>
            </Private>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
