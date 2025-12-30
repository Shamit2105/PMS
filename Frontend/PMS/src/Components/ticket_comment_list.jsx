import { useEffect, useState } from "react";
import api from "../api/axiosConfig";

function TicketCommentList({ projectId, storyId, ticketId }) {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    api
      .get(`/tickets/projects/${projectId}/stories/${storyId}/tickets/${ticketId}/comments/`)
      .then(res => setComments(res.data.results || res.data));
  }, [projectId, storyId, ticketId]);

  return (
    <div>
      <h4>Comments</h4>
      {comments.map(c => <p key={c.id}>{c.message}</p>)}
    </div>
  );
}

export default TicketCommentList;
