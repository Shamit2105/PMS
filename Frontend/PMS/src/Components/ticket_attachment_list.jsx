import { useEffect, useState } from "react";
import api from "../api/axiosConfig";

function TicketAttachmentList({ projectId, storyId, ticketId }) {
  const [attachments, setAttachments] = useState([]);

  useEffect(() => {
    api
      .get(`/tickets/projects/${projectId}/stories/${storyId}/tickets/${ticketId}/attachments/`)
      .then(res => setAttachments(res.data.results || res.data));
  }, [projectId, storyId, ticketId]);

  return (
    <div>
      <h4>Attachments</h4>
      {attachments.map(a => (
        <a key={a.id} href={a.file} target="_blank">File</a>
      ))}
    </div>
  );
}

export default TicketAttachmentList;
