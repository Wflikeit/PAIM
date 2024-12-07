import React from "react";
import { Typography, Button, List, ListItem } from "@mui/material";

interface CartProps {
  items: { name: string; price: number }[];
  onCheckout: () => void;
}

const Cart: React.FC<CartProps> = ({ items, onCheckout }) => {
  return (
    <div>
      <Typography variant="h6">Koszyk</Typography>
      <List>
        {items.map((item, index) => (
          <ListItem key={index}>
            {item.name} - {item.price} zł
          </ListItem>
        ))}
      </List>
      <Button onClick={onCheckout} variant="contained" color="primary">
        Złóż zamówienie
      </Button>
    </div>
  );
};

export default Cart;
