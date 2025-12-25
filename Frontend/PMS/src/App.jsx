import SignUpForm from "./Components/signup"
import Home from "./Components/home"
import { Route,BrowserRouter,Routes } from "react-router-dom"
import Login from "./Components/login";
function App() {
  return (
    <BrowserRouter>
      <h1 className="text-3xl font-bold underline text-[#000080]">
        Project Management System
      </h1>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUpForm />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


