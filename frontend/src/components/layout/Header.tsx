import ProfilePhotoWrapper from "../layout/ProfilePhotoWrapper";
import Logo from "./Logo.tsx";
import React from "react";
import HeaderLink from "./HeaderLink.tsx";

const Header = () => {
  return (
    <header className="layout__header">
      <Logo />
      <div
        style={{
          display: "flex",
          color: "blue",
          gap: "2rem",
          alignItems: "center",
        }}
      >
        <HeaderLink to="/" text="Home" />
        <HeaderLink to="/contact" text="Contact" />
        <HeaderLink to="/about" text="About" />
        <HeaderLink to="/" text="Products" />
      </div>
      <ProfilePhotoWrapper user={undefined} />
    </header>
  );
};

export default Header;