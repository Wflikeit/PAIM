import { Outlet, useLocation } from "react-router-dom";
import React from "react";

const Main = () => {
  const location = useLocation();

  return (
    <main
      style={{
        gridColumn: location.pathname === "/" ? "2/3" : "1/3",
        gridRow: "2/3",
        height: "100%",
        overflowY: "scroll",
        maxHeight: "100%",
      }}
    >
      <Outlet />
    </main>
  );
};

export default Main;