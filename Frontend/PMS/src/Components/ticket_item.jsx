import { useState } from "react";
import TicketDetail from "./ticket_detail";

function TicketItem({ ticket, projectId, storyId }) {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <div onClick={() => setOpen(!open)}>
        <b>{ticket.title}</b> — {ticket.status}
      </div>

      {open && (
        <TicketDetail
          projectId={projectId}
          storyId={storyId}
          ticketId={ticket.id}
        />
      )}
    </div>
  );
}

export default TicketItem;
