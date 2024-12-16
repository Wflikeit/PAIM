import React from "react";

const NotFound: React.FC = () => {
  return (
    <div style={{ textAlign: "center", padding: "50px", color: "black" }}>
      <h1>404 - Page Not Found</h1>
      <p>Sorry, the page you are looking for does not exist.</p>
      <p>
        You may have mistyped the address or the page may have moved.{" "}
        <a href="/" style={{ color: "blue", textDecoration: "underline" }}>
          Go back to the homepage.
        </a>
      </p>
    </div>
  );
};

export default NotFound;
