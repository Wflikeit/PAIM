import React from "react";
import { Box } from "@mui/material";
import HeaderLink from "./HeaderLink.tsx";
import ShoppingCartMiniature from "./ShoppingCart.tsx";
import ProfilePhotoWrapper from "./ProfilePhotoWrapper.tsx";

export interface LoggedInUser {
  email: string;
  role: string;
}

export default function UserActionsWrapper({ user }: { user?: LoggedInUser }) {
  return (
    <div className="icon__wrapper">
      <Box sx={{ display: "flex", gap: 2, height: "3rem" }}>
        {!user && (
          <>
            <HeaderLink to="/login" text="Login" />
            <HeaderLink to="/register" text="Register" />
          </>
        )}

        {user && <ProfilePhotoWrapper />}
        <ShoppingCartMiniature />
      </Box>
    </div>
  );
}