import { useState } from "react";
import { signup } from "../api/authApi";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function Signup() {

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const handleSubmit = async (e) => {

    e.preventDefault();

    // password validation
    if (password.length < 8) {

      toast.error("Password must be at least 8 characters long");

      return;

    }

    try {

      await signup({
        email,
        password
      });

      toast.success("Account created successfully");

      navigate("/login");

    } catch (err) {

      if (err.response?.status === 400) {

        toast.error("User already exists");

      } else {

        toast.error("Signup failed");

      }

    }

  };

  return (

    <div className="auth-page">

      <div className="auth-card">

        <h2>Create Account</h2>

        <p>Sign up to manage inventory</p>

        <form onSubmit={handleSubmit}>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password (minimum 8 characters)"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />

          <button type="submit">
            Create Account
          </button>

        </form>

      </div>

    </div>

  );

}

export default Signup;