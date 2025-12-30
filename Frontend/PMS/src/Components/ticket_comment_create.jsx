import { useState } from "react";
import api from "../api/axiosConfig";

function TicketCommentCreate({ projectId, storyId, ticketId }) {
  const [message, setMessage] = useState("");

  async function submit() {
    await api.post(
      `/tickets/projects/${projectId}/stories/${storyId}/tickets/${ticketId}/comments/`,
      { ticket: ticketId, message }
    );
    setMessage("");
  }

  return (
    <div>
      <input value={message} onChange={e => setMessage(e.target.value)} />
      <button onClick={submit}>Comment</button>
    </div>
  );
}

export default TicketCommentCreate;
