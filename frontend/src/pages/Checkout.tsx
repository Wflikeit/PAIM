import React, { useState } from "react";
import { Box, Button, Stack, TextField, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store.ts";
import WestIcon from "@mui/icons-material/West";
import { LocalizationProvider, StaticDatePicker } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { useMutation } from "react-query";
import { placeOrder } from "../api/ordersApi.ts";

const CheckoutPage: React.FC = () => {
  const cartItems = useSelector((state: RootState) => state.cart.items);
  const currency: string = "zł";

  const [shippingAddress, setShippingAddress] = useState({
    fullName: "",
    address: "",
    city: "",
    postalCode: "",
    country: "",
  });

  const [deliveryDate, setDeliveryDate] = useState<Date | null>(null);
  const [errors, setErrors] = useState({
    fullName: "",
    address: "",
    city: "",
    postalCode: "",
    country: "",
    deliveryDate: "",
  });

  const busyDays = [
    new Date(2025, 0, 10),
    new Date(2025, 0, 15),
    new Date(2025, 0, 20),
  ];

  const isDayDisabled = (date: Date) => {
    return busyDays.some(
      (busyDay) =>
        busyDay.getDate() === date.getDate() &&
        busyDay.getMonth() === date.getMonth() &&
        busyDay.getFullYear() === date.getFullYear(),
    );
  };

  const validateFields = () => {
    const postalCodeRegex = /^[0-9]{2}-[0-9]{3}$/;


    const newErrors = {
      fullName: shippingAddress.fullName ? "" : "Full name is required",
      address: shippingAddress.address ? "" : "Address is required",
      city: shippingAddress.city ? "" : "City is required",
      postalCode: shippingAddress.postalCode
        ? postalCodeRegex.test(shippingAddress.postalCode)
        ? ""
        : "Invalid postal code format (e.g., 12-345)"
      : "Postal code is required",
      country: shippingAddress.country ? "" : "Country is required",
      deliveryDate: deliveryDate ? "" : "Delivery date is required",
    };
    setErrors(newErrors);
    return Object.values(newErrors).every((error) => !error);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setShippingAddress({ ...shippingAddress, [name]: value });
  };

  const {
    mutate: placeOrderMutation,
    isLoading,
    isError,
    isSuccess,
  } = useMutation(placeOrder, {
    onSuccess: (data) => {
      console.log("Order placed successfully:", data);
    },
    onError: (error) => {
      console.error("Error placing order:", error);
    },
  });

  const handleOrderPlacement = () => {
    if (!validateFields()) {
      console.error("Validation failed: Fields are missing");
      return;
    }

    const orderDetails = {
      cartItems,
      shippingAddress,
      deliveryDate,
    };

    placeOrderMutation(orderDetails);
  };
  const totalPrice = cartItems.reduce(
    (total, item) => total + item.price * item.quantity,
    0,
  );

  return (
    <Box
      sx={{
        padding: "16px",
        color: "black",
        margin: "10dvh auto",
        maxWidth: "50rem",
        minWidth: "30rem",
      }}
    >
      <Typography variant="h4" sx={{ fontWeight: 600, marginBottom: "1.5rem" }}>
        Checkout
      </Typography>

      {cartItems.length === 0 ? (
        <Typography>Your cart is empty</Typography>
      ) : (
        <Box>
          <Typography variant="h6" sx={{ marginBottom: "1rem" }}>
            Order Summary
          </Typography>
          <Box
            sx={{
              maxHeight: "20dvh",
              overflowY: "auto",
              marginBottom: "2rem",
              border: "1px solid lightgray",
              borderRadius: "8px",
              padding: "1rem",
            }}
          >
            {cartItems.map((item) => (
              <Typography key={item.id}>
                {item.name} - {item.quantity} x {item.price} {currency}
              </Typography>
            ))}
          </Box>

          <Typography variant="h6" sx={{ marginBottom: "1rem" }}>
            Shipping Address
          </Typography>

          <Stack spacing={2}>
            <TextField
              fullWidth
              label="Full Name"
              name="fullName"
              value={shippingAddress.fullName}
              onChange={handleInputChange}
              error={!!errors.fullName}
              helperText={errors.fullName}
            />
            <TextField
              fullWidth
              label="Address"
              name="address"
              value={shippingAddress.address}
              onChange={handleInputChange}
              error={!!errors.address}
              helperText={errors.address}
            />
            <Stack direction="row" spacing={2}>
              <TextField
                fullWidth
                label="City"
                name="city"
                value={shippingAddress.city}
                onChange={handleInputChange}
                error={!!errors.city}
                helperText={errors.city}
              />
              <TextField
                fullWidth
                label="Postal Code"
                name="postalCode"
                value={shippingAddress.postalCode}
                onChange={handleInputChange}
                error={!!errors.postalCode}
                helperText={errors.postalCode}
              />
            </Stack>
            <TextField
              fullWidth
              label="Country"
              name="country"
              value={shippingAddress.country}
              onChange={handleInputChange}
              error={!!errors.country}
              helperText={errors.country}
            />
          </Stack>

          <Typography
            variant="h6"
            sx={{ marginTop: "2rem", marginBottom: "1rem" }}
          >
            Select Delivery Date
          </Typography>

          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <StaticDatePicker
              displayStaticWrapperAs="desktop"
              value={deliveryDate}
              onChange={(newValue) => setDeliveryDate(newValue)}
              shouldDisableDate={isDayDisabled}
            />
          </LocalizationProvider>
          {errors.deliveryDate && (
            <Typography color="red">Delivery date is required</Typography>
          )}

          <Typography variant="h6" sx={{ marginTop: "2rem", fontWeight: 600 }}>
            Total Price: {totalPrice.toFixed(2)} {currency}
          </Typography>

          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: "2rem",
            }}
          >
            <Link
              to="/"
              style={{
                textDecoration: "none",
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                color: "green",
              }}
            >
              <WestIcon fontSize="small" /> Continue Shopping
            </Link>
            <Button
              variant="contained"
              color="primary"
              onClick={handleOrderPlacement}
              disabled={isLoading}
            >
              {isLoading ? "Placing Order..." : "Place Order"}
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default CheckoutPage;
