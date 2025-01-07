import React, { useEffect, useState } from "react";
import axios from "axios";
import NotFound from "./NotFound";
import {TOKEN_KEY} from "../auth/authService.ts";

const Admin = () => {
  const [message, setMessage] = useState("");
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const token = localStorage.getItem(TOKEN_KEY); // Retrieve the token from localStorage
        const response = await axios.get("http://127.0.0.1:8002/admin/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setMessage(response.data.message);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 403) {
          setHasError(true);
        } else {
          console.error("Unexpected error:", err);
        }
      }
    };

    fetchAdminData();
  }, []);

  if (hasError) {
    return <NotFound />;
  }

  return (
      <div>
        <h1>Admin Page</h1>
        <p>{message}</p>
      </div>
  );
};

export default Admin;
