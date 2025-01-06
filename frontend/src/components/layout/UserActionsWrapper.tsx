import React from "react";
import { Box } from "@mui/material";
import HeaderLink from "./HeaderLink.tsx";
import ShoppingCartMiniature from "./ShoppingCart.tsx";
import ProfilePhotoWrapper from "./ProfilePhotoWrapper.tsx";

export interface LoggedInUser {
  fullname: string;
  token: string;
  role: string;
}

interface UsersActionWrapperProps {
  user?: LoggedInUser;
}

const UserActionsWrapper: React.FC<UsersActionWrapperProps> = ({ user }) => {

  return (
    <div className="icon__wrapper">
      <Box sx={{ display: "flex", gap: 2, height: "3rem" }}>
        {!user && (
          <>
            <HeaderLink to="/login" text="Login" />
            <HeaderLink to="/register" text="Register" />
          </>
        )}

        {user && <ProfilePhotoWrapper user={user} />}
        <ShoppingCartMiniature />
      </Box>
    </div>
  );
};

export default UserActionsWrapper;
