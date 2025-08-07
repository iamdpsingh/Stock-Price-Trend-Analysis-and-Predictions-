import React, { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

const AdminDashboard = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      <p>Welcome, Admin! You have full access to the system.</p>

      {/* Add your admin-specific features/components here */}

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;
