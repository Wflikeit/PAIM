import React, { useState } from "react";
import { Button, TextField, Typography } from "@mui/material";
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
      const response = await axios.post("http://localhost:8000/api/register", {
        email,
        password,
      });

      const { role } = response.data;

      localStorage.setItem("user_role", role);

      if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/");
      }
    } catch (error) {
      setError("Invalid email or password");
    }
  };

  const handleRegisterRedirect = () => {
    navigate("/register");
  };

  return (
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
  );
};

export default LoginForm;