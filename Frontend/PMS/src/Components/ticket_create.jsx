import { useEffect, useState } from "react";
import api from "../api/axiosConfig";

function TicketCreate({ projectId, storyId, onCreate }) {
  const [members, setMembers] = useState([]);

  const [form, setForm] = useState({
    title: "",
    description: "",
    assigned_member: "",
    status: "todo",
    priority: "medium",
    type: "task",
    due_date: "",
  });

  /* ================= LOAD PROJECT MEMBERS ================= */
  useEffect(() => {
    api
      .get(`/projects/projects/${projectId}/project-members/`)
      .then(res => setMembers(res.data.results || res.data))
      .catch(console.error);
  }, [projectId]);

  /* ================= CREATE TICKET ================= */
  async function handleCreate() {
    if (!form.assigned_member || !form.due_date) {
      alert("Assigned member and due date are required");
      return;
    }

    try {
      const res = await api.post(
        `/tickets/projects/${projectId}/stories/${storyId}/tickets/`,
        {
          story: storyId,
          ...form,
        }
      );

      onCreate(res.data.data);

      setForm({
        title: "",
        description: "",
        assigned_member: "",
        status: "todo",
        priority: "medium",
        type: "task",
        due_date: "",
      });
    } catch (err) {
      alert(err.response?.data?.error || "Error creating ticket");
    }
  }

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Create Ticket</h3>

      <input
        placeholder="Title"
        value={form.title}
        onChange={e => setForm({ ...form, title: e.target.value })}
      />

      <textarea
        placeholder="Description"
        value={form.description}
        onChange={e => setForm({ ...form, description: e.target.value })}
      />

      {/* ASSIGNED MEMBER */}
      <select
        value={form.assigned_member}
        onChange={e =>
          setForm({ ...form, assigned_member: e.target.value })
        }
      >
        <option value="">Assign to</option>
        {members.map(m => (
          <option key={m.id} value={m.id}>
            {m.user} — {m.role}
          </option>
        ))}
      </select>

      {/* STATUS */}
      <select
        value={form.status}
        onChange={e => setForm({ ...form, status: e.target.value })}
      >
        <option value="todo">Todo</option>
        <option value="in_progress">In Progress</option>
        <option value="review">Review</option>
        <option value="done">Done</option>
        <option value="blocked">Blocked</option>
      </select>

      {/* PRIORITY */}
      <select
        value={form.priority}
        onChange={e => setForm({ ...form, priority: e.target.value })}
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      {/* TYPE */}
      <select
        value={form.type}
        onChange={e => setForm({ ...form, type: e.target.value })}
      >
        <option value="task">Task</option>
        <option value="bug">Bug</option>
      </select>

      {/* DUE DATE */}
      <input
        type="date"
        value={form.due_date}
        onChange={e =>
          setForm({ ...form, due_date: e.target.value })
        }
      />

      <button onClick={handleCreate}>Create Ticket</button>
    </div>
  );
}

export default TicketCreate;
