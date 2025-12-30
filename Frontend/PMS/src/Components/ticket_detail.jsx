import TicketCommentList from "./ticket_comment_list";
import TicketCommentCreate from "./ticket_comment_create";
import TicketAttachmentList from "./ticket_attachment_list";
import TicketAttachmentCreate from "./ticket_attachment_create";

function TicketDetail({ projectId, storyId, ticketId }) {
  return (
    <div style={{ marginLeft: 20 }}>
      <TicketCommentList
        projectId={projectId}
        storyId={storyId}
        ticketId={ticketId}
      />
      <TicketCommentCreate
        projectId={projectId}
        storyId={storyId}
        ticketId={ticketId}
      />

      <TicketAttachmentList
        projectId={projectId}
        storyId={storyId}
        ticketId={ticketId}
      />
      <TicketAttachmentCreate
        projectId={projectId}
        storyId={storyId}
        ticketId={ticketId}
      />
    </div>
  );
}

export default TicketDetail;
