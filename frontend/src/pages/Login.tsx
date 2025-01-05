import React from "react";
import LoginForm from "../components/LoginForm";
import { Box } from "@mui/material";

const Login = () => {
  return (
    <Box
      sx={{
        margin: "auto",
        maxWidth: " 36rem",
        minHeight: "100dvh",
        display: "grid",
        placeItems: "center",
      }}
    >
      <Box>
        <h1 style={{ color: "black" }}>Sign in</h1>
        <LoginForm />
      </Box>
    </Box>
  );
};

export default Login;