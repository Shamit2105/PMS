import SignUpForm from "./Components/signup"
import Home from "./Components/home"
import { Route,BrowserRouter,Routes } from "react-router-dom"
import Login from "./Components/login";
import Profile from "./Components/profile";
import ProtectedRoute from "./Components/protected_routes";
import Projects from "./Components/project_list";
import AddressForm from "./Components/address_page";
import CreateProject from "./Components/project_create";
import ProjectDetail from "./Components/project_detail"
import StoryDetail from "./Components/story_detail";
import AddressPage from "./Components/address_page";

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
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute> } />
        <Route path="/projects" element={<ProtectedRoute><Projects /></ProtectedRoute> } />
        <Route path="/projects/upsert" element={<ProtectedRoute><CreateProject /></ProtectedRoute> } />
        <Route path="/profile/address" element={<ProtectedRoute><AddressForm /></ProtectedRoute> } />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/projects/:projectId/stories/:storyId" element={<StoryDetail />}/>
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;


