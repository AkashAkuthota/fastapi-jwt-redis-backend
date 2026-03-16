import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { toast } from "react-toastify";

function Navbar() {

  const { token, role, logout } = useContext(AuthContext);

  const navigate = useNavigate();

  const handleLogout = async () => {

    await logout();

    toast.info("Logged out");

    navigate("/login");

  };

  return (

    <nav className="navbar">

      <div className="logo">
        FastAPI Inventory
      </div>

      <div className="nav-links">

        <Link to="/">Products</Link>

        <Link to="/cart">Cart</Link>

        {role === "admin" && (
          <Link to="/admin">Admin</Link>
        )}

        {!token && (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}

        {token && (
          <button onClick={handleLogout}>
            Logout
          </button>
        )}

      </div>

    </nav>

  );

}

export default Navbar;