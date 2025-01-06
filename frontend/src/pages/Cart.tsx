import React from "react";
import { Box, Button, List, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../redux/store.ts";
import { clearCart, removeFromCart } from "../model/cardItem.ts";

const CartPage: React.FC = () => {
  const navigate = useNavigate();
  const cartItems = useSelector((state: RootState) => state.cart.items); // Access Redux state
  const dispatch = useDispatch();

  // Debugging log
  console.log("Cart items in CartPage:", cartItems);

  // Function to handle removing an item from the cart
  const handleRemove = (id: string) => {
    dispatch(removeFromCart(id));
  };

  // Function to handle clearing the cart
  const handleClear = () => {
    dispatch(clearCart());
  };

  // Calculate the total price from the Redux cart items
  const totalPrice = cartItems.reduce(
    (total, item) => total + item.price * item.quantity,
    0,
  );
    const state = useSelector((state: RootState) => state);
    console.log("Entire Redux state:", state);


    return (
    <Box
      sx={{
        padding: "16px",
        color: "black",
        margin: "20dvh auto",
        maxWidth: "50rem",
        minWidth: "30rem",
      }}
    >
      <Typography variant="h4" gutterBottom>
        Cart
      </Typography>
      {cartItems.length === 0 ? ( // Check the Redux cart items
        <Typography>Your cart is empty</Typography>
      ) : (
        <>
          <List>
            {cartItems.map((item) => {
              console.log("Rendering item:", item); // Debugging log
              return (
                <Box
                  key={item.id}
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "1rem",
                  }}
                >
                  <Typography>
                    {item.name} x{item.quantity} - {item.price.toFixed(2)} zł
                  </Typography>
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={() => handleRemove(item.id)}
                  >
                    Remove
                  </Button>
                </Box>
              );
            })}
          </List>
          <Typography variant="h6" sx={{ marginTop: "1rem" }}>
            Total: {totalPrice.toFixed(2)} zł
          </Typography>
          <Button
            variant="contained"
            color="error"
            onClick={handleClear}
            sx={{ marginTop: "1rem" }}
          >
            Clear Cart
          </Button>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: "1.5rem",
            }}
          >
            <Button
              variant="outlined"
              onClick={() => navigate("/")}
              sx={{ flexGrow: 1, marginRight: "1rem" }}
            >
              Continue Shopping
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={() => console.log("Proceeding to checkout...")}
              sx={{ flexGrow: 1 }}
            >
              Checkout
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
};

export default CartPage;
