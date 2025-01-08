import React from "react";
import { Box, Button, Typography } from "@mui/material";

interface CartSummaryProps {
  totalPrice: number;
  onContinueShopping: () => void;
  onProceedToCheckout: () => void;
}

const CartSummary: React.FC<CartSummaryProps> = ({
  totalPrice,
  onContinueShopping,
  onProceedToCheckout,
}) => {
  return (
    <Box sx={{ marginTop: "16px" }}>
      <Typography variant="h6" style={{ color: "black" }}>
        In total: ${totalPrice.toFixed(2)}
      </Typography>
      <Box sx={{ marginTop: "16px" }}>
        <Button
          className="continue-shopping"
          onClick={() => onContinueShopping()}
          variant="contained"
          color="primary"
        >
          Continue shopping
        </Button>
        <Button
          className="checkout"
          onClick={onProceedToCheckout}
          variant="contained"
          color="secondary"
        >
          Checkout
        </Button>
      </Box>
    </Box>
  );
};

export default CartSummary;
