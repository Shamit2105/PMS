import { useState,useEffect } from "react";
import api from "../api/axiosConfig";
import TicketCreate from "./ticket_create";
import TicketItem from "./ticket_item";

function TicketList({projectId,storyId})
{
    const [tickets,setTickets] = useState([]);
    useEffect(()=>
    {
        api.get(`/tickets/projects/${projectId}/stories/${storyId}/tickets/`)
        .then(res=>setTickets(res.data.results || res.data));
    },[projectId,storyId]);

    return (
        <div>
            <h2> Tickets </h2>
            {tickets.map(t=> (
                <TicketItem key={t.id} ticket={t} projectId={projectId} storyId={storyId} />
            ))}

            <TicketCreate projectId={projectId} storyId={storyId} onCreate = {t=> setTickets(prev=>[...prev,t])} />
        </div>
    )
}
export default TicketList;