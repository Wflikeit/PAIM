import React from "react";
import {
  Box,
  Button,
  IconButton,
  List,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../redux/store.ts";
import {
  clearCart,
  removeFromCart,
  updateCartItemQuantity,
} from "../model/cardItem.ts";

const CartPage: React.FC = () => {
  const navigate = useNavigate();
  const cartItems = useSelector((state: RootState) => state.cart.items); // Access Redux state
  const dispatch = useDispatch();

  // Function to handle removing an item from the cart
  const handleRemove = (id: string) => {
    dispatch(removeFromCart(id));
  };

  // Function to handle clearing the cart
  const handleClear = () => {
    dispatch(clearCart());
  };

  // Function to handle quantity change
  const handleQuantityChange = (id: string, quantity: number) => {
    if (quantity > 0) {
      dispatch(updateCartItemQuantity({ id, quantity }));
    }
  };

  // Calculate the total price from the Redux cart items
  const totalPrice = cartItems.reduce(
    (total, item) => total + item.price * item.quantity,
    0,
  );

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
            {cartItems.map((item) => (
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
                  {item.name} - {item.price.toFixed(2)} zł
                </Typography>
                <Box sx={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <IconButton
                    onClick={() =>
                      handleQuantityChange(item.id, item.quantity - 1)
                    }
                    sx={{
                      width: "40px",
                      height: "40px",
                      borderRadius: "4px",
                      "&:hover": {
                        backgroundColor: "#f0f0f0",
                      },
                    }}
                  >
                    -
                  </IconButton>
                  <TextField
                    value={item.quantity}
                    type="number"
                    size="small"
                    onChange={(e) =>
                      handleQuantityChange(
                        item.id,
                        parseInt(e.target.value, 10) || 1,
                      )
                    }
                    sx={{
                      width: "50px",
                      textAlign: "center",
                      "& input[type=number]::-webkit-outer-spin-button, & input[type=number]::-webkit-inner-spin-button":
                        {
                          WebkitAppearance: "none",
                          margin: 0,
                        },
                      "& input[type=number]": {
                        MozAppearance: "textfield",
                      },
                      "& input": {
                        padding: "8px", // Match the IconButton padding
                        textAlign: "center",
                      },
                    }}
                  />
                  <IconButton
                    onClick={() =>
                      handleQuantityChange(item.id, item.quantity + 1)
                    }
                    sx={{
                      width: "40px",
                      height: "40px",
                      borderRadius: "4px",
                      "&:hover": {
                        backgroundColor: "#f0f0f0",
                      },
                    }}
                  >
                    +
                  </IconButton>
                </Box>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => handleRemove(item.id)}
                >
                  Remove
                </Button>
              </Box>
            ))}
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