import { Badge } from "@mui/material";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import React from "react";
import { Link } from "react-router-dom";



const ShoppingCartMiniature = () => {
  return (
    <Link to="/cart" className="cart" sx={{ margin: "auto" }}>
      <Badge
        badgeContent={5} // Hardcoded value of items in the cart
        color="secondary"
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        sx={{
          "& .MuiBadge-badge": {
            fontSize: "1rem",
            height: "1.2rem",
            minWidth: "1.2rem",
            transform: "translate(-25%, 25%)",
            backgroundColor: "#ea2323",
          },
        }}
      >
        <ShoppingCartIcon sx={{ fontSize: "2.5rem", color: "#177c1b" }} />
      </Badge>
    </Link>
  );
};

export default ShoppingCartMiniature;