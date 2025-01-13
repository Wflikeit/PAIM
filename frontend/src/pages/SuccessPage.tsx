import React, { useEffect, useState } from "react";
import { Box, Card, CardActions, CardContent, Typography } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { clearCart } from "../model/cardItem.ts";
import { clearCheckoutFormData } from "../model/checkoutFormData.ts";
import { clearOrderId } from "../model/order.ts";
import axios from "axios";
import { RootState } from "../redux/store.ts";
import {BACKEND_URL} from "../hooks/useProducts.ts";

const SuccessPage: React.FC = () => {
  const dispatch = useDispatch();
  const orderId = useSelector((state: RootState) => state.order.orderId);
  const [error, setError] = useState<string | null>(null);
  const [orderCompleted, setOrderCompleted] = useState(false);

  // Clear the cart on mount
  useEffect(() => {
    const completeOrder = async () => {
      if (!orderId) {
        setError("Order ID not found");
        return;
      }

      try {
        await axios.put(`${BACKEND_URL}/api/orders/${orderId}/complete`);
        setOrderCompleted(true);
        dispatch(clearOrderId());
      } catch (error) {
        setError("Failed to complete the order.");
        console.error(error);
      }
    };
    completeOrder();

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
          {orderCompleted ? (
            <>
              <Typography variant="h5" fontWeight="bold" gutterBottom>
                Order Successful!
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Thank you for your purchase! Your order has been placed
                successfully.
              </Typography>
            </>
          ) : error ? (
            <h2>Error: {error}</h2>
          ) : (
            <h2>Completing your order...</h2>
          )}
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
            style={{
              borderRadius: 2,
              textTransform: "none",
              padding: 3,
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