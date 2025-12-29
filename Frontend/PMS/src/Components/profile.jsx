import api from "../api/axiosConfig";
import { useEffect,useState } from "react";
import { useNavigate } from "react-router-dom";

function Profile()
{
    const navigate = useNavigate();
    const [editing,setEditing]= useState(false);
    const [profileId, setProfileId] = useState(null);
    const [formData,setFormData]=useState({
        username: "",
        first_name: "",
        last_name: "",
        dob: "",
        contact_number: "",
        address: "",
    });
    const [error,setError]=useState("");

    useEffect(()=>
    {
        async function fetchProfile()
        {
            try
            {
                const res = await api.get("/users/profile/");
                const data=res.data.results[0]; 
                setProfileId(data.id);
                setFormData({
                    username: data.username,
                    first_name: data.first_name,
                    last_name: data.last_name,
                    dob: data.dob,
                    contact_number: data.contact_number,
                    address: data.address?(data.address):'Not provided',
                });
            }
            catch (error)
            {
                setError("Failed to load profile");
                console.error(error);

            }

        }
        fetchProfile();
    },[]);

    function handleChange(e) 
    {
        const { name, value } = e.target;
        setFormData(prev => 
        ({
            ...prev,
            [name]: value,
        }));
    }
    async function handleSave() {
        try {
        await api.patch(`/users/profile/${profileId}/`, formData);
        setEditing(false);
        } catch (err) {
        setError("Failed to update profile");
        }
    }

    return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Profile</h2>

      {error && <p className="text-red-600">{error}</p>}

      <input
        name="username"
        value={formData.username}
        disabled
        className="input"
      />

      <input
        name="first_name"
        value={formData.first_name}
        onChange={handleChange}
        disabled={!editing}
        className="input"
      />

      <input
        name="last_name"
        value={formData.last_name}
        onChange={handleChange}
        disabled={!editing}
        className="input"
      />

      <input
        type="date"
        name="dob"
        value={formData.dob || ""}
        onChange={handleChange}

        disabled
        className="input"
      />

      <input
        name="contact_number"
        value={formData.contact_number}
        onChange={handleChange}
        disabled={!editing}
        className="input"
      />
      

      {!editing ? (
        <button className="px-4 py-2" onClick={() => setEditing(true)}>Edit</button>
      ) : (
        <div className="flex gap-2">
          <button className="px-4 py-2" onClick={handleSave}>Save</button>
          <button className="px-4 py-2" onClick={() => setEditing(false)}>Cancel</button>
        </div>
      )}
      <button className="px-4 py-2" type="submit" onClick={()=>{navigate('/')}}>Home</button>
      <button className="px-4 py-2" type="submit" onClick={()=>{navigate('/profile/address')}}>Address</button>
    </div>
  );



};
export default Profile;

