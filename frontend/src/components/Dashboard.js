import React, { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { logout, role } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="container">
      <h1>Dashboard</h1>
      <p>Welcome! You are logged in as a <strong>{role}</strong>.</p>

      {role === "admin" && (
        <div>
          <h2>Admin Panel</h2>
          {/* Add admin-specific components or links here */}

          <button onClick={() => navigate("/admin")}>Go to Admin Settings</button>
        </div>
      )}
      <br />

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;
