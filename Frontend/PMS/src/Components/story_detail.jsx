import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";

function StoryDetail() {
  const { projectId, storyId } = useParams();
  const navigate = useNavigate();

  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState("");

  useEffect(() => {
    api
      .get(`/projects/projects/${projectId}/stories/${storyId}/`)
      .then(res => {
        setStory(res.data);
        setStatus(res.data.status);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [projectId, storyId]);

  
  const updateStatus = async () => {
    try {
      await api.patch(
        `/projects/projects/${projectId}/stories/${storyId}/`,
        { status }
      );

      alert("Status updated");

      const res = await api.get(
        `/projects/projects/${projectId}/stories/${storyId}/`
      );
      setStory(res.data);
    } catch (err) {
      alert("Error updating status");
    }
  };

  if (loading) return <h2>Loading...</h2>;
  if (!story) return <h2>Story not found</h2>;

  return (
    <div>
      <h1>{story.title}</h1>
      <p>{story.description}</p>

      <p>
        <b>Status:</b> {story.status}
      </p>

      <h3>Update Status</h3>
      <select value={status} onChange={e => setStatus(e.target.value)}>
        <option value="todo">Todo</option>
        <option value="in_progress">In Progress</option>
        <option value="review">Review</option>
        <option value="done">Done</option>
        <option value="blocked">Blocked</option>
      </select>

      <button onClick={updateStatus}>Update</button>

      <hr />

      <button onClick={() => navigate(-1)}>Back</button>
    </div>
  );
}

export default StoryDetail;
