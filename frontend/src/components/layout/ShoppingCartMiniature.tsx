import { Badge } from "@mui/material";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import React from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import {RootState} from "../../redux/store.ts";

const ShoppingCartMiniature = () => {
  // Select cart items from Redux store
  const cartItems = useSelector((state: RootState) => state.cart.items);

  // Calculate total quantity of items in the cart
  const totalQuantity = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
      <Link
          to="/cart"
          className="cart"
          style={{ margin: "auto" }}
      >
        <Badge
            badgeContent={totalQuantity} // Dynamic quantity from Redux store
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
