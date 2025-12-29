import { useState,useEffect } from "react";
import api from "../api/axiosConfig";
import { useNavigate } from "react-router-dom";


function CreateProject({initialData=null})
{
    const [formData,setFormData]=useState(
        {
            name:initialData?.name||"",
            description: initialData?.description || "",
            start_date: initialData?.start_date || "",
            end_date: initialData?.end_date || "",
            status: initialData?.status || "todo",

        }

    );
    const navigate=useNavigate();

    function handleChange(e) 
    {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    }

    async function handleSubmit(e)
    {
        e.preventDefault();
        try
        {
            if (initialData)
            {
                await api.patch(`/projects/projects/${initialData.id}/`,formData);
            }
            else
                await api.post("/projects/projects/",formData);
            navigate("/projects");

        }
        catch(error)
        {
            console.error(error.response?.data);
        }
    }
    return (
        <form onSubmit={handleSubmit} className="space-y-4">
        <input
            name="name"
            placeholder="Project name"
            value={formData.name}
            onChange={handleChange}
            required
        />

        <textarea
            name="description"
            placeholder="Description"
            value={formData.description}
            onChange={handleChange}
        />

        <input
            type="date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
        />

        <input
            type="date"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
        />

        <select name="status" value={formData.status} onChange={handleChange}>
            <option value="todo">Todo</option>
            <option value="in_progress">In Progress</option>
            <option value="review">Review</option>
            <option value="done">Done</option>
            <option value="blocked">Blocked</option>
        </select>

        <button type="submit">
            {initialData ? "Update Project" : "Create Project"}
        </button>
        </form>
    );

}
export default CreateProject;