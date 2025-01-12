import React, { useEffect } from "react";
import { Box, Card, CardActions, CardContent, Typography } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { clearCart } from "../model/cardItem.ts";
import { clearCheckoutFormData } from "../model/checkoutFormData.ts"; // Adjust the import path to your cartSlice

const SuccessPage: React.FC = () => {
  const dispatch = useDispatch();

  // Clear the cart on mount
  useEffect(() => {
    dispatch(clearCart());
    dispatch(clearCheckoutFormData());
  }, [dispatch]);

  return (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#177c1b",
      }}
    >
      <Card
        sx={{
          maxWidth: 400,
          width: "100%",
          textAlign: "center",
          borderRadius: 4,
          boxShadow: 4,
        }}
      >
        <CardContent>
          <CheckCircleIcon
            sx={{
              fontSize: 60,
              color: "#4caf50",
              marginBottom: 2,
            }}
          />
          <Typography variant="h5" fontWeight="bold" gutterBottom>
            Order Successful!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Thank you for your purchase! Your order has been placed
            successfully.
          </Typography>
        </CardContent>
        <CardActions
          sx={{
            justifyContent: "center",
            paddingBottom: 2,
          }}
        >
          <Link
            to="/"
            color="primary"
            sx={{
              borderRadius: 2,
              textTransform: "none",
              paddingX: 3,
            }}
          >
            Return to Home
          </Link>
        </CardActions>
      </Card>
    </Box>
  );
};

export default SuccessPage;