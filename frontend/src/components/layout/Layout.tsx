import React from "react";
import { Box } from "@mui/material";
import Main from "./Main.tsx";
import Sidebar from "./Sidebar.tsx";
import Footer from "./Footer.tsx";
import Header from "./Header.tsx";

const Layout = (): React.JSX.Element => {
  return (
    <Box
      gridTemplateRows={"auto 1fr auto"}
      gridTemplateColumns={"220px auto"}
      display={"grid"}
      style={{ minHeight: "100vh" }}
    >
      <Sidebar />
      <Header />
      <Main />
      <Footer />
    </Box>
  );
};

export default Layout;