import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import RegisterForm from "../../src/pages/Register";
import registerClients from "../../src/hooks/registerClients";

// Mock the `registerClients` hook
jest.mock("../../src/hooks/registerClients", () => ({
    __esModule: true,
    default: jest.fn(() => ({
        addClient: jest.fn(),
    })),
}));

describe("Register", () => {
    const mockAddClient = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        (registerClients as jest.Mock).mockReturnValue({ addClient: mockAddClient });
    });

    it("renders the form with all input fields and submit button", () => {
        render(<RegisterForm />);

        expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/NIP/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Nazwa firmy/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/adres płatności/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/adres dostawy/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/hasło/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/zamówienia/i)).toBeInTheDocument();
        expect(screen.getByText(/register/i)).toBeInTheDocument();
    });

    it("shows validation error when required fields are empty", () => {
        render(<RegisterForm />);

        const registerButton = screen.getByText(/register/i);
        fireEvent.click(registerButton);

        expect(screen.getByText(/proszę wypełnić wszystkie pola/i)).toBeInTheDocument();
    });

    it("submits the form successfully when all fields are valid", async () => {
        render(<RegisterForm />);

        fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
        fireEvent.change(screen.getByLabelText(/nip/i), { target: { value: "123456789" } });
        fireEvent.change(screen.getByLabelText(/nazwa firmy/i), { target: { value: "Test Company" } });
        fireEvent.change(screen.getByLabelText(/adres płatności/i), {
            target: { value: "123 Billing St, City, Country" },
        });
        fireEvent.change(screen.getByLabelText(/adres dostawy/i), {
            target: { value: "456 Shipping Ln, City, Country" },
        });
        fireEvent.change(screen.getByLabelText(/hasło/i), { target: { value: "password123" } });
        fireEvent.change(screen.getByLabelText(/zamówienia/i), { target: { value: "[]" } });

        const registerButton = screen.getByText(/register/i);
        fireEvent.click(registerButton);

        await waitFor(() => {
            expect(mockAddClient).toHaveBeenCalledWith({
                email: "test@example.com",
                payment_address: "123 Billing St, City, Country",
                delivery_address: "456 Shipping Ln, City, Country",
                nip: "123456789",
                password: "password123",
                company_name: "Test Company",
                orders: "[]",
            });
        });

        expect(screen.queryByText(/proszę wypełnić wszystkie pola/i)).not.toBeInTheDocument();
    });

    it("shows error when the API call fails", async () => {
        mockAddClient.mockRejectedValueOnce(new Error("Registration failed"));

        render(<RegisterForm />);

        fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
        fireEvent.change(screen.getByLabelText(/nip/i), { target: { value: "123456789" } });
        fireEvent.change(screen.getByLabelText(/nazwa firmy/i), { target: { value: "Test Company" } });
        fireEvent.change(screen.getByLabelText(/adres płatności/i), {
            target: { value: "123 Billing St, City, Country" },
        });
        fireEvent.change(screen.getByLabelText(/adres dostawy/i), {
            target: { value: "456 Shipping Ln, City, Country" },
        });
        fireEvent.change(screen.getByLabelText(/hasło/i), { target: { value: "password123" } });
        fireEvent.change(screen.getByLabelText(/zamówienia/i), { target: { value: "[]" } });

        const registerButton = screen.getByText(/register/i);
        fireEvent.click(registerButton);

        await waitFor(() => {
            expect(screen.getByText(/wystąpił błąd podczas rejestracji klienta/i)).toBeInTheDocument();
        });
    });
});
