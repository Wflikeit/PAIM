import { Link } from "@mui/material";
import React from "react";

type HeaderLinkProps = {
  to: string;
  text: string;
};

const HeaderLink: React.FC<HeaderLinkProps> = ({ to, text }) => {
  return (
    <Link
      href={to}
      sx={{ color: "blue", fontSize: "1.25rem", margin: "auto" }}
      underline="none"
    >
      {text}
    </Link>
  );
};

export default HeaderLink;