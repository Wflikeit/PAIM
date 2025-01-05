import React, { useState } from "react";
import { TextField, Button, Container, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const LoginForm = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!email || !password) {
      setError("Please fill in all fields");
      return;
    }

    try {
      // Create FormData to handle the POST request
      const formData = new FormData();
      formData.append("username", email); // Backend expects "username" for email
      formData.append("password", password);


      const response = await axios.post("http://127.0.0.1:8000/admin/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      console.log("Response data:", response.data);

      const { access_token } = response.data;
      const tokenPayload = JSON.parse(
        atob(access_token.split(".")[1]) // Decode JWT payload
      );
      const role = tokenPayload.role;

      // Store the token and role in localStorage
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("user_role", role);

      // Redirect based on role
      if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/");
      }
    } catch (error) {
      console.error("Login failed:", error);
      setError("Invalid email or password");
    }
  };

  const handleRegisterRedirect = () => {
    navigate("/register");
  };

  return (
    <Container className="buttons-container">
      <form onSubmit={handleSubmit}>
        <TextField
          label="Email"
          variant="outlined"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button
          type="submit"
          className="login"
          variant="contained"
          color="primary"
        >
          Login
        </Button>
        <Button
          type="button"
          className="register"
          onClick={handleRegisterRedirect}
          variant="contained"
          color="secondary"
        >
          Register
        </Button>
      </form>
    </Container>
  );
};

export default LoginForm;
