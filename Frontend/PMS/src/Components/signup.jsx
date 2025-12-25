import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function SignUpForm() {
  const navigate = useNavigate(); 
  

  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirm_password: "",
    first_name: "",
    last_name: "",
    dob: "",
    contact_number: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    setError("");
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await axios.post(
        "http://localhost:8000/users/signup/",
        formData
      );

      const loginRes = await axios.post(
        "http://localhost:8000/users/login/",
        {
          username: formData.username,
          password: formData.password,
        }
      );

      localStorage.setItem("access", loginRes.data.access);
      localStorage.setItem("refresh", loginRes.data.refresh);

      setError("");
      setSuccess("Signup successful!");

      navigate("/home"); 

    } catch (err) {
      setSuccess("");
      setError(err.response?.data?.detail || "Signup Failed");
    }
  }

  return (
    <div>

    <form
      className="flex flex-col gap-4 max-w-md mx-auto p-6 bg-white rounded-xl shadow-md"
      onSubmit={handleSubmit}
      >
      <h2 className="text-2xl font-semibold text-center">
        Sign Up
      </h2>

      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-600">{success}</p>}

      <input name="username" placeholder="Username" onChange={handleChange} />
      <input type="password" name="password" placeholder="Password" onChange={handleChange} />
      <input type="password" name="confirm_password" placeholder="Confirm Password" onChange={handleChange} />

      <input name="first_name" placeholder="First Name" onChange={handleChange} />
      <input name="last_name" placeholder="Last Name" onChange={handleChange} />

      <input type="date" name="dob" onChange={handleChange} />
      <input name="contact_number" placeholder="Contact Number" onChange={handleChange} />

      <button type="submit">Sign Up</button>

    </form>
      <p>
        Already have an account?{" "}
        <button
            className="submit"onClick=
            { 
                ()=>
                {
                    navigate("/login")
                }
            }
        >
          Login
        </button>
      </p>
    </div>
  );
}

export default SignUpForm;
