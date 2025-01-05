import React, { useState } from "react";
import Popover from "@mui/material/Popover";
import { red } from "@mui/material/colors";
import { Badge, Box, Link } from "@mui/material";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import HeaderLink from "./HeaderLink.tsx";

export interface LoggedInUser {
  email: string;
  role: string;
}

export default function ProfilePhotoWrapper({ user }: { user?: LoggedInUser }) {
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div className="icon__wrapper">
      <Box sx={{ display: "flex", gap: 2, height: "3rem" }}>
        {!user && (
          <>
            <HeaderLink to="/login" text="Login" />
            <HeaderLink to="/register" text="Register" />
          </>
        )}

        {user && (
          <>
            <button
              className="photo__wrapper"
              style={{
                backgroundColor: red[500],
                margin: "auto",
              }}
              onClick={handleClick}
            >
              {user.email ? user.email[0].toUpperCase() : "U"}{" "}
            </button>

            <Popover
              id={id}
              open={open}
              anchorEl={anchorEl}
              onClose={handleClose}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
              }}
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              sx={{
                marginTop: "1.3rem",
                borderRadius: "1rem",
              }}
            >
              <button className="sign__out__button">Sign out</button>
            </Popover>
          </>
        )}
        <Link href="/cart" className="cart" sx={{ margin: "auto" }}>
          <Badge
            badgeContent={5} // Hardcoded value of items in the cart
            color="secondary"
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "left",
            }}
            sx={{
              "& .MuiBadge-badge": {
                fontSize: "1rem",
                height: "1.2rem",
                minWidth: "1.2rem",
                transform: "translate(-25%, 25%)",
              },
            }}
          >
            <ShoppingCartIcon sx={{ fontSize: "2.5rem" }} />
          </Badge>
        </Link>
      </Box>
    </div>
  );
}