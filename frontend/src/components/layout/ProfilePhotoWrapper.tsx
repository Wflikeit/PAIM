import React, {useState} from "react";
import Popover from "@mui/material/Popover";
import {red} from "@mui/material/colors";
import {Box, Button} from "@mui/material";
import {useNavigate} from "react-router-dom";
//
// import { getInitialsFromEmail } from '../reservation/ReservationUtils';
//
// import { useCustomNavigation } from 'src/hooks/NavigationHook';
// import { LoggedInUser, TOKEN_KEY } from 'src/auth/authService';
// import { randomColorFor } from 'src/values/colors';

export interface LoggedInUser {
  email: string;
  role: string;
}

export default function ProfilePhotoWrapper({ user }: { user?: LoggedInUser }) {
  const [anchorEl, setAnchorEl] = useState<
    HTMLButtonElement | null | undefined
  >(null);
  // const { navigateToLoginPage } = useCustomNavigation();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  // const handleLogoutClick = () => {
  //     localStorage.removeItem(TOKEN_KEY);
  //     navigateToLoginPage();
  // };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  // const avatarColor = randomColorFor(user?.email as string);

  return (
    <div className="icon__wrapper">
      {/*<NavWrapper></NavWrapper>*/}

      <Box sx={{ display: "flex", gap: 2, height: "3rem" }}>
        <Button
          className="cart"
          color="inherit"
          onClick={() => handleNavigate("/cart")}
        >
          Cart
        </Button>

        <Button
          className="login"
          color="inherit"
          onClick={() => handleNavigate("/login")}
        >
          Login
        </Button>
        <Button
          className="login"
          color="inherit"
          onClick={() => handleNavigate("/register")}
        >
          Register
        </Button>
        <button
          className="photo__wrapper"
          style={{ backgroundColor: `${red}`, margin: "auto" }}
          onClick={handleClick}
        >
          {user ? "WF" : null}
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
            borderRadius: "1rem !important",
          }}
        >
          {/*<button className="sign__out__button" onClick={handleLogoutClick}>*/}
          {/*    Sign out*/}
          {/*</button>*/}
          <button className="sign__out__button">Sign out</button>
        </Popover>
      </Box>
    </div>
  );
}
