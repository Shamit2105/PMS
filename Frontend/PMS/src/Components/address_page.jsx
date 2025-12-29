import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";
import AddressForm from "./address_form";

function AddressPage() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    api
      .get("/users/profile/me/")
      .then(res => {
        setProfile(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  const address = profile?.address;

  return (
    <div className="max-w-md mx-auto p-6 space-y-4 bg-white shadow rounded">

      <h2 className="text-xl font-semibold">Address</h2>

      {/* VIEW MODE */}
      {address && !editing && (
        <>
          <div className="border p-4 rounded bg-gray-50 space-y-1">
            <p>{address.primary_address}</p>
            {address.secondary_address && <p>{address.secondary_address}</p>}
            <p>{address.city_name}</p>
            <p>{address.pincode}</p>
          </div>

          <button
            type="button"
            onClick={() => setEditing(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded"
          >
            Edit Address
          </button>
        </>
      )}

      {/* NO ADDRESS */}
      {!address && !editing && (
        <button
          type="button"
          onClick={() => setEditing(true)}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Add Address
        </button>
      )}

      {/* FORM MODE */}
      {editing && (
        <AddressForm
          existingAddress={address}
          onSuccess={() => {
            setEditing(false);
            api.get("/users/profile/me/")
              .then(res => setProfile(res.data));
          }}
        />
      )}

      <button
        type="button"
        onClick={() => navigate(-1)}
        className="px-4 py-2 border rounded"
      >
        Back
      </button>
    </div>
  );
}

export default AddressPage;
