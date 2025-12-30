import api from "../api/axiosConfig";

function TicketAttachmentCreate({ projectId, storyId, ticketId }) {
  async function upload(e) {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);
    formData.append("ticket", ticketId);

    await api.post(
      `/tickets/projects/${projectId}/stories/${storyId}/tickets/${ticketId}/attachments/`,
      formData
    );
  }

  return <input type="file" onChange={upload} />;
}

export default TicketAttachmentCreate;
