import { red } from "@mui/material/colors";
import Popover from "@mui/material/Popover";
import React, { useState } from "react";
import {LoggedInUser} from "./UserActionsWrapper.tsx";

interface ProfilePhotoWrapperProps{
    user: LoggedInUser
}
const ProfilePhotoWrapper:React.FC<ProfilePhotoWrapperProps> = ({ user }) => {
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
    <>
      <button
        className="photo__wrapper"
        style={{
          backgroundColor: red[500],
          margin: "auto",
        }}
        onClick={handleClick}
      >
        {user.fullname ? user.fullname[0].toUpperCase() : "U"}
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
  );
};

export default ProfilePhotoWrapper;