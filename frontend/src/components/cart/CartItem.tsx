import React from "react";
import {Typography} from "@mui/material";
import QuantityInput from "./QuantityInput.tsx";
import {CartItem} from "../../model/cardItem.ts";

// Define the interface for the cart item
interface CartItemProps {
  item: CartItem;
  handleQuantityChange: (id: string, quantity: number) => void;
}

const currency: string = "zł";

const CartItem: React.FC<CartItemProps> = ({ item, handleQuantityChange }) => {
  return (
    <div
      key={item.id}
      style={{
        display: "grid",
        gridTemplateColumns: "3fr 1fr 1fr 1fr",
        gap: "1rem",
        alignItems: "center",
        padding: "1rem 0",
      }}
    >
      <Typography>{item.name}</Typography>
      <QuantityInput
        productID={item.id}
        quantity={item.quantity}
        handleQuantityChange={handleQuantityChange}
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      />
      <Typography sx={{ textAlign: "center" }}>
        {item.price.toFixed(2)} {currency}
      </Typography>
      <Typography sx={{ textAlign: "center" }}>
        {(item.quantity * item.price).toFixed(2)} {currency}
      </Typography>
    </div>
  );
};

export default CartItem;
