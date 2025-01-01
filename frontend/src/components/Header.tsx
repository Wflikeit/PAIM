import React from "react";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Header: React.FC = () => {
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography
          variant="h4"
          sx={{
            flexGrow: 1,
            cursor: "pointer",
            "&:hover": {
              textDecoration: "none",
              color: "inherit",
            },
          }}
          onClick={() => handleNavigate("/")}
        >
          Wholesale Fruits
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Button
            className="cart"
            color="inherit"
            onClick={() => handleNavigate("/cart")}
          >
            Cart
          </Button>
          <Button
            className="about"
            color="inherit"
            onClick={() => handleNavigate("/about")}
          >
            About
          </Button>
          <Button
            className="contact"
            color="inherit"
            onClick={() => handleNavigate("/contact")}
          >
            Contact
          </Button>
          <Button
            className="login"
            color="inherit"
            onClick={() => handleNavigate("/login")}
          >
            Login
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
