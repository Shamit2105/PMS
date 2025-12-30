import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";
import TicketList from "./ticket_list";

function StoryDetail() {
  const { projectId, storyId } = useParams();
  const navigate = useNavigate();

  const [story, setStory] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get(`/projects/projects/${projectId}/stories/${storyId}/`)
      .then(res => {
        setStory(res.data);
        setStatus(res.data.status);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [projectId, storyId]);

  async function updateStatus() {
    await api.patch(
      `/projects/projects/${projectId}/stories/${storyId}/`,
      { status }
    );
    setStory(prev => ({ ...prev, status }));
  }

  if (loading) return <p>Loading...</p>;
  if (!story) return <p>Story not found</p>;

  return (
    <div>
      <h1>{story.title}</h1>
      <p>{story.description}</p>

      <select value={status} onChange={e => setStatus(e.target.value)}>
        <option value="todo">Todo</option>
        <option value="in_progress">In Progress</option>
        <option value="review">Review</option>
        <option value="done">Done</option>
        <option value="blocked">Blocked</option>
      </select>

      <button onClick={updateStatus}>Update Status</button>

      <hr />

      <TicketList projectId={projectId} storyId={storyId} />

      <button onClick={() => navigate(-1)}>Back</button>
    </div>
  );
}

export default StoryDetail;
