import { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import { Link } from "react-router-dom";

const NavBar = () => {
  const { role, logout } = useContext(AuthContext);

  return (
    <nav>
      <Link to="/dashboard">Dashboard</Link>
      {role === "admin" && <Link to="/admin">Admin</Link>}
      <button onClick={logout}>Logout</button>
    </nav>
  );
};
