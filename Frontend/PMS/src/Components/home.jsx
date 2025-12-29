import { useEffect, useState } from "react";
import handleLogout from "./logout";
import { useNavigate } from "react-router-dom";

function Home() {
  const [isAuth, setIsAuth] = useState(false);
  const navigate = useNavigate();
  useEffect(() => {
    setIsAuth(!!localStorage.getItem("access"));
  }, []);

  return (
    <div>
      {isAuth ? (
        <div>
        <h1>Welcome to Home</h1>
        <button className="px-4 py-2" type="submit" onClick={handleLogout}>Logout</button>
        <button className="px-4 py-2" type="submit" onClick={()=>{navigate("/profile")}}>Profile</button>
        <button type="submit" onClick={()=>{navigate('/projects')}}>Projects</button>
        </div>
      ) : (
        <div>
        <button className="px-4 py-2" onClick={()=> {navigate("/login")}}>Login</button>
        <button className="px-4 py-2" onClick={()=> {navigate("/signup")}}>Sign Up</button>
        </div>
      )}
    </div>
  );
}

export default Home;
