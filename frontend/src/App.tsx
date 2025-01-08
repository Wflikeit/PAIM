import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/ProductsList";
import Login from "./pages/Login";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Admin from "./pages/Admin";
import CartPage from "./pages/Cart";
import RegisterForm from "./pages/Register";
import NotFound from "./pages/NotFound";
import Layout from "./components/layout/Layout";
import { ProtectedRouteWrapper } from "./auth/ProtectedRouterWrapper.tsx";
import { UserRole } from "./auth/UserRole.ts";
import React from "react";
import { EnsureAuth } from "./auth/EnsureAuth.tsx";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <EnsureAuth />

      <Routes>
        <Route element={<Layout />}>
          <Route
            path="/*"
            element={
              <ProtectedRouteWrapper
                allowedRoles={[UserRole.ADMIN, UserRole.CLIENT]}
              >
                <Routes>
                  <Route path="/" element={<Home />} />

                  <Route path="/checkout" element={<CartPage />} />
                  <Route path="/admin" element={<Admin />} />
                </Routes>
              </ProtectedRouteWrapper>
            }
          />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Route>
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;