import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import { Link, useNavigate } from "react-router-dom";

function Projects() {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api
      .get("/projects/projects/")
      .then(res => {
        setProjects(res.data.results);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Projects</h2>

      <ul>
        {projects.map(p => (
          <li
            key={p.project_members[0].project}
            style={{ cursor: "pointer", color: "blue" }}
            onClick={() =>
              navigate(`/projects/${p.project_members[0].project}`)
            }
          >
            {p.name}
          </li>
        ))}
      </ul>

      <button onClick={() => navigate("/")}>Home</button>
      <button onClick={() => navigate("/projects/upsert")}>
        Create Project
      </button>
    </div>
  );
}

export default Projects;
