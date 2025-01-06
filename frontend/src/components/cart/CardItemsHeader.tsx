import { Typography } from "@mui/material";
import React from "react";

const CartItemsHeader: React.FC = () => {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "3fr 1fr 1fr 1fr",
        gap: "1rem",
        alignItems: "center",
        padding: "1.5rem 0",
        color: "gray",
      }}
    >
      <Typography sx={{ fontWeight: 550 }}>PRODUCT DETAILS</Typography>
      <Typography sx={{ fontWeight: 550, textAlign: "center" }}>
        QUANTITY
      </Typography>
      <Typography sx={{ fontWeight: 550, textAlign: "center" }}>
        PRICE
      </Typography>
      <Typography sx={{ fontWeight: 550, textAlign: "center" }}>
        TOTAL
      </Typography>
    </div>
  );
};
export default CartItemsHeader;