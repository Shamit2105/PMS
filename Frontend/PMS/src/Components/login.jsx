import { useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  }

  // login handler
  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    try {
      const resp = await axios.post(
        "http://localhost:8000/users/login/",
        formData
      );

      localStorage.setItem("access", resp.data.access);
      localStorage.setItem("refresh", resp.data.refresh);

      navigate("/", { replace: true });

    } catch (err) {
      setError("Invalid credentials");
    }
  }

  return (
      <div>

      <form className="flex flex-col gap-4 max-w-md mx-auto p-6 bg-white rounded-xl shadow-md" onSubmit={handleLogin}>
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        name="username"
        placeholder="Username"
        onChange={handleChange}
        />

      <input
        type="password"
        name="password"
        placeholder="Password"
        onChange={handleChange}
      />
      <button type="submit">Login</button>

    </form>
      If not signed up, create your account here:<button className="submit" onClick={()=>{navigate('/signup')}}>Sign Up</button>
    </div>
  );
}

export default Login;
