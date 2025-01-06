import React from "react";
import {Button, ListItem, ListItemText} from "@mui/material"; // Define the interface for the cart item

// Define the interface for the cart item
interface CartItemProps {
  id: string;
  name: string;
  price: number;
  quantity: number;
  removeFromCart: (id: string) => void;
}

const CartItem: React.FC<CartItemProps> = (props) => {
  return (
    <ListItem
      sx={{
        marginBottom: "16px",
        display: "flex",
        justifyContent: "space-between",
      }}
    >
      <ListItemText
        style={{ color: "black" }}
        primary={`${props.name} x${props.quantity}`}
        secondary={`Price: $${props.price.toFixed(2)} x${props.quantity}`}
      />
      <Button
        className="delete"
        onClick={() => props.removeFromCart(props.id)}
        color="secondary"
        style={{ color: "black" }}
      >
        Delete
      </Button>
    </ListItem>
  );
};

export default CartItem;
