import { createContext, useState } from "react";
import { login as loginApi, logout as logoutApi } from "../api/authApi";

export const AuthContext = createContext();

function getRoleFromToken(token) {

  if (!token) return null;

  try {

    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");

    const payload = JSON.parse(atob(base64));

    return payload.role;

  } catch {

    return null;

  }

}

export function AuthProvider({ children }) {

  const storedToken = localStorage.getItem("access_token");

  const [token,setToken] = useState(storedToken);
  const [role,setRole] = useState(getRoleFromToken(storedToken));

  const login = async (credentials) => {

    const res = await loginApi(credentials);

    const accessToken = res.data.access_token;

    localStorage.setItem("access_token", accessToken);

    setToken(accessToken);

    setRole(getRoleFromToken(accessToken));

  };

  const logout = async () => {

    try {

      await logoutApi();

    } catch (err) {

      console.warn("Logout API failed");

    }

    localStorage.removeItem("access_token");

    setToken(null);

    setRole(null);

  };

  return (

    <AuthContext.Provider
      value={{
        token,
        role,
        login,
        logout
      }}
    >

      {children}

    </AuthContext.Provider>

  );

}