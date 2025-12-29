import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";

function ProjectDetail() {
  const { id } = useParams(); // project UUID
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);

  // forms
  const [memberUserId, setMemberUserId] = useState("");
  const [memberRole, setMemberRole] = useState("developer");

  const [story, setStory] = useState({
    title: "",
    description: "",
    status: "todo",
  });

  // fetch project
  useEffect(() => {
    api
      .get(`/projects/projects/${id}/`)
      .then(res => {
        setProject(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  // add member
  const addMember = async () => {
    try {
      await api.post("projects/projects/"+ id +"project-members/", {
        project: id,
        user: memberUserId,
        role: memberRole,
      });

      alert("Member added");
      setMemberUserId("");
      // refresh project
      const res = await api.get(`/projects/projects/${id}/`);
      setProject(res.data);
    } catch (err) {
      alert(err.response?.data?.message || "Error adding member");
    }
  };

  // create story
  const createStory = async () => {
    try {
      await api.post("/projects/projects/"+id+"/stories/", {
        project: id,
        ...story,
      });

      alert("Story created");
      setStory({ title: "", description: "", status: "todo" });

      const res = await api.get(`/projects/projects/${id}/`);
      setProject(res.data);
    } catch (err) {
      alert("Error creating story");
    }
  };

  if (loading) return <h2>Loading...</h2>;
  if (!project) return <h2>Project not found</h2>;

  return (
    <div>
      <h1>{project.name}</h1>
      <p>{project.description}</p>
      <p>Status: {project.status}</p>

      <hr />

      {/* MEMBERS */}
      <h2>Project Members</h2>
      <ul>
        {project.project_members.map(pm => (
          <li key={pm.id}>
            User #{pm.user_first_name} — {pm.role}
          </li>
        ))}
      </ul>

      <h3>Add Member</h3>
      <input
        placeholder="User ID"
        value={memberUserId}
        onChange={e => setMemberUserId(e.target.value)}
      />
      <select
        value={memberRole}
        onChange={e => setMemberRole(e.target.value)}
      >
        <option value="owner">Owner</option>
        <option value="developer">Developer</option>
        <option value="viewer">Viewer</option>
      </select>
      <button onClick={addMember}>Add</button>

      <hr />

      {/* STORIES */}
      <h2>Stories / Tickets</h2>
      <ul>
        {project.stories.map(s => (
          <li 
            key={s.id} style={{ cursor: "pointer" }}
            onClick={() =>
                navigate(`/projects/${id}/stories/${s.id}`)
            }
          >
            <b>{s.title}</b> — {s.status}
          </li>
        ))}
      </ul>

      <h3>Create Story</h3>
      <input
        placeholder="Title"
        value={story.title}
        onChange={e => setStory({ ...story, title: e.target.value })}
      />
      <textarea
        placeholder="Description"
        value={story.description}
        onChange={e => setStory({ ...story, description: e.target.value })}
      />
      <select
        value={story.status}
        onChange={e => setStory({ ...story, status: e.target.value })}
      >
        <option value="todo">Todo</option>
        <option value="in_progress">In Progress</option>
        <option value="review">Review</option>
        <option value="done">Done</option>
        <option value="blocked">Blocked</option>
      </select>

      <button onClick={createStory}>Create Story</button>

      <hr />

      <button onClick={() => navigate("/")}>Home</button>
    </div>
  );
}

export default ProjectDetail;
