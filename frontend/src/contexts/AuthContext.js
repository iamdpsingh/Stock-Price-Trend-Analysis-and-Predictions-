import React, { createContext, useState, useEffect } from "react";
import { jwtDecode as jwt_decode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("jwtToken"));
  const [role, setRole] = useState(null);

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwt_decode(token);
        setRole(decoded.role || "user");
      } catch {
        setRole(null);
      }
    } else {
      setRole(null);
    }
  }, [token]);

  const login = (jwt) => {
    localStorage.setItem("jwtToken", jwt);
    setToken(jwt);
  };

  const logout = () => {
    localStorage.removeItem("jwtToken");
    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
