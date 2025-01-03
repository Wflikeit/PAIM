import React from "react";
import LoginForm from "../components/LoginForm";
import {Box, Container} from "@mui/material";

const Login = () => {
  return (
    <Box sx={{ margin: "auto", maxWidth: " 36rem", minHeight: "100dvh" }}>
      <Container sx={{ marginY: "8rem" }}>
        <h1 style={{ color: "black" }}>Sign in</h1>
        <LoginForm />
      </Container>
    </Box>
  );
};

export default Login;