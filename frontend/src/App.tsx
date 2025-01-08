import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/ProductsList";
import Login from "./pages/Login";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Admin from "./pages/Admin";
import CartPage from "./pages/Cart";
import RegisterForm from "./pages/Register";
import NotFound from "./pages/NotFound";
import Layout from "./components/layout/Layout";
import CheckoutPage from "./pages/Checkout.tsx";

const App: React.FC = () => {
  return (
      <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/login" element={<Login />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
  );
};

export default App;
