import { useEffect, useState } from "react";
import api from "../api/axiosConfig";

function AddressForm({ onSuccess, existingAddress }) {
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);

  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedState, setSelectedState] = useState("");
  const [selectedCity, setSelectedCity] = useState("");

  const [isPrefilling, setIsPrefilling] = useState(false);

  const [addressData, setAddressData] = useState({
    primary_address: "",
    secondary_address: "",
    pincode: "",
  });

  useEffect(() => {
    if (!existingAddress) return;

    setIsPrefilling(true);

    setAddressData({
      primary_address: existingAddress.primary_address || "",
      secondary_address: existingAddress.secondary_address || "",
      pincode: existingAddress.pincode || "",
    });

    setSelectedCountry(existingAddress.country_id);
    setSelectedState(existingAddress.state_id);
    setSelectedCity(existingAddress.city_id);

    setTimeout(() => setIsPrefilling(false), 0);
  }, [existingAddress]);

  useEffect(() => {
    api
      .get("/misc/countries/")
      .then(res => setCountries(res.data.results))
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedCountry || isPrefilling) return;

    api
      .get(`/misc/states/?country=${selectedCountry}`)
      .then(res => setStates(res.data.results))
      .catch(console.error);

    setSelectedState("");
    setCities([]);
  }, [selectedCountry, isPrefilling]);

  useEffect(() => {
    if (!selectedState || isPrefilling) return;

    api
      .get(`/misc/cities/?state=${selectedState}`)
      .then(res => setCities(res.data.results))
      .catch(console.error);

    setSelectedCity("");
  }, [selectedState, isPrefilling]);

  function handleChange(e) {
    const { name, value } = e.target;
    setAddressData(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (!selectedCity) {
      alert("Please select a city");
      return;
    }
    try {
        console.log(" typeof selectedCity:", typeof selectedCity);
        console.log(" selectedCity:", selectedCity);
        await api.patch("/users/profile/me/", {
        address: {
          ...addressData,
          city: selectedCity, 
        },
      });

      alert("Address saved successfully");
      if (onSuccess) onSuccess();

    } catch (err) {
      console.error(err.response?.data || err.message);
      alert("Failed to save address");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">

      {/* COUNTRY */}
      <select
        value={selectedCountry}
        onChange={e => setSelectedCountry(e.target.value)}
        required
      >
        <option value="">Select Country</option>
        {countries.map(c => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>

      {/* STATE */}
      <select
        value={selectedState}
        onChange={e => setSelectedState(e.target.value)}
        disabled={!selectedCountry}
        required
      >
        <option value="">Select State</option>
        {states.map(s => (
          <option key={s.id} value={s.id}>
            {s.name}
          </option>
        ))}
      </select>

      {/* CITY */}
      <select
        value={selectedCity}
        onChange={e => setSelectedCity(e.target.value)}
        disabled={!selectedState}
        required
      >
        <option value="">Select City</option>
        {cities.map(c => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>

      {/* ADDRESS FIELDS */}
      <input
        name="primary_address"
        placeholder="Primary Address"
        value={addressData.primary_address}
        onChange={handleChange}
        required
      />

      <input
        name="secondary_address"
        placeholder="Secondary Address (optional)"
        value={addressData.secondary_address}
        onChange={handleChange}
      />

      <input
        name="pincode"
        placeholder="Pincode"
        value={addressData.pincode}
        onChange={handleChange}
        required
      />

      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Save Address
      </button>
    </form>
  );
}

export default AddressForm;
