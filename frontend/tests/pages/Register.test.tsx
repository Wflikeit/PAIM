import React from "react";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import RegisterForm from "../../src/pages/Register";
import registerClients from "../../src/hooks/registerClients";

// Mock the `registerClients` hook
jest.mock("../../src/hooks/registerClients", () => ({
  __esModule: true,
  default: jest.fn(() => ({
    addClient: jest.fn().mockResolvedValue({}), // Simulate successful API call
  })),
}));

describe("RegisterForm", () => {
  const mockAddClient = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (registerClients as jest.Mock).mockReturnValue({
      addClient: mockAddClient,
    });
  });

  it("submits the form successfully when all fields are valid", async () => {
    render(<RegisterForm />);

    // Fill out the form fields
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/NIP/i), {
      target: { value: "123456789" },
    });
    fireEvent.change(screen.getByLabelText(/Nazwa firmy/i), {
      target: { value: "Test Company" },
    });
    fireEvent.change(screen.getByLabelText(/Adres płatności/i), {
      target: { value: "123 Billing St, City, Country" },
    });
    fireEvent.change(screen.getByLabelText(/Adres dostawy/i), {
      target: { value: "456 Shipping Ln, City, Country" },
    });
    fireEvent.change(screen.getByLabelText(/Hasło/i), {
      target: { value: "password123" },
    });

    // Simulate clicking the register button
    const registerButton = screen.getByText(/Register/i);
    fireEvent.click(registerButton);

    // Wait for the mockAddClient to be called
    await waitFor(() => {
      expect(mockAddClient).toBeCalled();
    });

    // Ensure error message is not present
    expect(
      screen.queryByText(/Proszę wypełnić wszystkie pola/i),
    ).not.toBeInTheDocument();
  });

  it("shows validation error when required fields are empty", () => {
    render(<RegisterForm />);

    const registerButton = screen.getByText(/Register/i);
    fireEvent.click(registerButton);

    expect(
      screen.getByText(/Proszę wypełnić wszystkie pola/i),
    ).toBeInTheDocument();
  });

  it("renders the form with all input fields and submit button", () => {
    render(<RegisterForm />);

    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/NIP/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Nazwa firmy/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/adres płatności/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/adres dostawy/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/hasło/i)).toBeInTheDocument();
    expect(screen.getByText(/register/i)).toBeInTheDocument();
  });
});
