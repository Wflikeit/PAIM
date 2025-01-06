import UserActionsWrapper, {LoggedInUser} from "./UserActionsWrapper.tsx";
import Logo from "./Logo.tsx";
import React from "react";
import HeaderLink from "./HeaderLink.tsx";


const Header: React.FC = () => {
  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("user_role");
  const fullname = localStorage.getItem("fullname");


  const user: LoggedInUser | undefined =
    token && role && fullname ? { token, role, fullname } : undefined;

  console.log("Header user object:", user);

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
      <UserActionsWrapper user={user} />
    </header>
  );
};

export default Header;
