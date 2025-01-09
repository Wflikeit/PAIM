import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../src/App";

describe("App", () => {
    it("renders the Home page on default route", () => {
        render(
            <MemoryRouter initialEntries={["/"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Products List/i)).toBeInTheDocument(); // Replace with a unique element in `Home`
    });

    it("renders the About page on /about route", () => {
        render(
            <MemoryRouter initialEntries={["/about"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/About/i)).toBeInTheDocument(); // Replace with a unique element in `About`
    });

    it("renders the Contact page on /contact route", () => {
        render(
            <MemoryRouter initialEntries={["/contact"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Contact/i)).toBeInTheDocument(); // Replace with a unique element in `Contact`
    });

    it("renders the Cart page on /cart route", () => {
        render(
            <MemoryRouter initialEntries={["/cart"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Cart/i)).toBeInTheDocument(); // Replace with a unique element in `CartPage`
    });

    it("renders the Checkout page on /checkout route", () => {
        render(
            <MemoryRouter initialEntries={["/checkout"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Checkout/i)).toBeInTheDocument(); // Replace with a unique element in `CheckoutPage`
    });

    it("renders the Admin page on /admin route", () => {
        render(
            <MemoryRouter initialEntries={["/admin"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Admin/i)).toBeInTheDocument(); // Replace with a unique element in `Admin`
    });

    it("renders the Register page on /register route", () => {
        render(
            <MemoryRouter initialEntries={["/register"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Register/i)).toBeInTheDocument(); // Replace with a unique element in `RegisterForm`
    });

    it("renders the Login page on /login route", () => {
        render(
            <MemoryRouter initialEntries={["/login"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Login/i)).toBeInTheDocument(); // Replace with a unique element in `Login`
    });

    it("renders the NotFound page for an unknown route", () => {
        render(
            <MemoryRouter initialEntries={["/unknown"]}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Not Found/i)).toBeInTheDocument(); // Replace with a unique element in `NotFound`
    });
});
