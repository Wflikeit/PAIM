import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import About from "./pages/About";
import Contact from "./pages/Contact";
// import Header from "./components/Header";
import Admin from "./pages/Admin";
import CartPage from "./pages/Cart";
import RegisterForm from "./pages/Register";
import NotFound from "./pages/NotFound";
import Layout from "./components/layout/Layout.tsx";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route
            path="/"
            element={
              <>
                {/*<Header />*/}
                <Home />
              </>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route
            path="/about"
            element={
              <>
                {/*<Header />*/}
                <About />
              </>
            }
          />
          <Route
            path="/contact"
            element={
              <>
                {/*<Header />*/}
                <Contact />
              </>
            }
          />
          <Route
            path="/cart"
            element={
              <>
                {/*<Header />*/}
                <CartPage />
              </>
            }
          />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/admin" element={<Admin />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;