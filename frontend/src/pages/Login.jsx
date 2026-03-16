import { useState, useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function Login() {

  const { login, token } = useContext(AuthContext);

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  // Redirect if already logged in
  useEffect(() => {

    if (token) {
      navigate("/");
    }

  }, [token, navigate]);

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      await login({
        email,
        password
      });

      toast.success("Login successful");

      navigate("/");

    } catch (err) {

      if (err.response?.status === 401) {

        toast.error("Invalid email or password");

      } else {

        toast.error("Login failed. Try again.");

      }

    }

  };

  return (

    <div className="auth-page">

      <div className="auth-card">

        <h2>Login</h2>

        <p>Access your inventory account</p>

        <form onSubmit={handleSubmit}>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />

          <button type="submit">
            Login
          </button>

        </form>

      </div>

    </div>

  );

}

export default Login;