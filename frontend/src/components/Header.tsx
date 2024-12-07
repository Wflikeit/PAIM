import React from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Hurtownia Owoców
        </Typography>
        <Button onClick={handleLoginClick} color="inherit">
          Zaloguj się
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
