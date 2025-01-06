import React, { useState } from "react";
import { Box, Button, TextField, Typography } from "@mui/material";
import registerClients from "../hooks/registerClients";

const RegisterForm = () => {
  const { addClient } = registerClients();
  const [email, setEmail] = useState<string>("");
  const [payment_address, setPaymentAddress] = useState<string>("");
  const [delivery_address, setDeliveryAddress] = useState<string>("");
  const [nip, setNip] = useState<string>("");
  const [orders, setOrders] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [company_name, setCompanyName] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (
      !email ||
      !password ||
      !company_name ||
      !nip ||
      !payment_address ||
      !delivery_address
    ) {
      setError("Proszę wypełnić wszystkie pola");
      return;
    }

    setError("");

    const newClient = {
      email,
      payment_address,
      delivery_address,
      nip,
      orders,
      password,
      company_name,
    };

    console.log("Form data to be sent:", newClient);

    try {
      await addClient(newClient);
      console.log("Zarejestrowano:", newClient);

      setEmail("");
      setPaymentAddress("");
      setDeliveryAddress("");
      setNip("");
      setOrders("");
      setPassword("");
      setCompanyName("");
    } catch (error) {
      setError("Wystąpił błąd podczas rejestracji klienta: " + error);
    }
  };

  return (
    <Box
      sx={{
        padding: "16px",
        color: "black",
        margin: "5dvh auto",
        maxWidth: "30rem",
        minWidth: "20rem",
      }}
    >
      <Box>
        <form onSubmit={handleSubmit}>
          <Typography
            variant="h3"
            gutterBottom
            style={{ color: "black", textAlign: "center" }}
            sx={{ paddingTop: "60px" }}
            size={"small"}
          >
            Create account
          </Typography>

          <TextField
            label="Email"
            variant="outlined"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => {
              console.log("Email: " + e.target.value);
              setEmail(e.target.value);
            }}
            size={"small"}
          />

          <TextField
            label="NIP"
            variant="outlined"
            fullWidth
            margin="normal"
            value={nip}
            onChange={(e) => setNip(e.target.value)}
            size={"small"}
          />

          <TextField
            label="Nazwa firmy"
            variant="outlined"
            fullWidth
            margin="normal"
            value={company_name}
            onChange={(e) => setCompanyName(e.target.value)}
            size={"small"}
          />

          <TextField
            label="Adres płatności (oddziel przecinkami)"
            variant="outlined"
            fullWidth
            margin="normal"
            value={payment_address}
            onChange={(e) => setPaymentAddress(e.target.value)}
            size={"small"}
          />

          <TextField
            label="Adres dostawy (oddziel przecinkami)"
            variant="outlined"
            fullWidth
            margin="normal"
            value={delivery_address}
            onChange={(e) => setDeliveryAddress(e.target.value)}
            size={"small"}
          />

          <TextField
            label="Hasło"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            size={"small"}
          />

          {error && (
            <Typography variant="body2" color="error" gutterBottom>
              {error}
            </Typography>
          )}

          <Button
            type="submit"
            className="register"
            variant="contained"
            sx={{ backgroundColor: "#388e3c", marginTop: "1rem" }}
            fullWidth
            onChange={(e) => setOrders("zamowienie")}
          >
            Register
          </Button>
        </form>
      </Box>
    </Box>
  );
};

export default RegisterForm;