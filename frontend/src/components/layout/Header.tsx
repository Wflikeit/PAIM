import ProfilePhotoWrapper from "../layout/ProfilePhotoWrapper";
import Logo from "./Logo.tsx";
import React from "react";
import { Link } from "@mui/material";

const Header = () => {
  return (
    <header className="layout__header">
      <Logo />
      <div style={{ display: "flex", color: "blue", gap: "2rem", alignItems:"center" }}>
        <Link
          underline="none"
          sx={{ color: "blue", fontSize: "1.25rem" }}
          href="/"
        >
          Home
        </Link>
        <Link
          underline="none"
          sx={{ color: "blue", fontSize: "1.25rem" }}
          href="/contact"
        >
          Contact
        </Link>
        <Link
          underline="none"
          sx={{ color: "blue", fontSize: "1.25rem" }}
          href="/about"
        >
          About
        </Link>
        <Link
          underline="none"
          sx={{ color: "blue", fontSize: "1.25rem" }}
          href="/"
        >
          Products
        </Link>
      </div>
      <ProfilePhotoWrapper user={undefined} />
    </header>
  );
};

export default Header;