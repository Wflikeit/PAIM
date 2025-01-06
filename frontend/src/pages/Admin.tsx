import React, { useEffect, useState } from "react";
import axios from "axios";

const Admin = () => {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const token = localStorage.getItem("access_token"); // Retrieve the token from localStorage
        const response = await axios.get("http://127.0.0.1:8002/admin/", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token in the Authorization header
          },
        });
        setMessage(response.data.message); // Set the message from the backend
      } catch (err) {
        setError("You are not authorized to view this page.");
        console.error(err);
      }
    };

    fetchAdminData();
  }, []);

  if (error) {
    return (
      <div>
        <h1>Admin Page</h1>
        <p style={{ color: "red" }}>{error}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Admin Page</h1>
      <p>{message}</p>
    </div>
  );
};

export default Admin;