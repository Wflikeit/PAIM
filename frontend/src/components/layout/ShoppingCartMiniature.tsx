import { Badge } from "@mui/material";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import React from "react";
import { Link } from "react-router-dom";

const ShoppingCartMiniature = () => {
  return (
    <Link
      to="/cart"
      className="cart"
      style={{ margin: "auto", textDecoration: "none" }} // Ensure no underline
    >
      <Badge
        badgeContent={5} // Hardcoded value of items in the cart
        color="secondary"
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        sx={{
          "& .MuiBadge-badge": {
            fontSize: "1rem", // Badge text size
            height: "1.2rem", // Badge height
            minWidth: "1.2rem", // Badge width
            transform: "translate(-25%, 25%)", // Adjust position
            backgroundColor: "#ea2323", // Badge background color
            color: "white", // Badge text color
          },
        }}
      >
        <ShoppingCartIcon sx={{ fontSize: "2.5rem", color: "#177c1b" }} />
      </Badge>
    </Link>
  );
};

export default ShoppingCartMiniature;