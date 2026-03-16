import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { toast } from "react-toastify";

function Navbar() {

  const { token, role, logout } = useContext(AuthContext);

  const handleLogout = () => {
    logout();
    toast.info("Logged out");
  };

  return (

    <nav className="navbar">

      <div className="logo">
        FastAPI Inventory
      </div>

      <div className="nav-links">

        <Link to="/">Products</Link>

        <Link to="/cart">Cart</Link>

        {/* Admin panel visible only to admins */}
        {role === "admin" && (
          <Link to="/admin">Admin</Link>
        )}

        {/* If NOT logged in */}
        {!token && (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}

        {/* If logged in */}
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