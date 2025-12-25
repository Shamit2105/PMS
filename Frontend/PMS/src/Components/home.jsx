import { useEffect, useState } from "react";
import handleLogout from "./logout";

function Home() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    setIsAuth(!!localStorage.getItem("access"));
  }, []);

  return (
    <div>
      {isAuth ? (
        <div>
        <h1>Welcome to Home</h1>
        <button type="submit" onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <h1>Please login</h1>
      )}
    </div>
  );
}

export default Home;
