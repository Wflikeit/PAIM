import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, useNavigate } from "react-router-dom";
import axios from "axios";
import LoginForm from "../../../src/components/login/LoginForm";

// Mock axios and useNavigate
jest.mock("axios");
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: jest.fn(),
}));

describe("LoginForm", () => {
    const mockNavigate = jest.fn();
    const mockedAxios = axios as jest.Mocked<typeof axios>;

    beforeEach(() => {
        jest.clearAllMocks();
        (useNavigate as jest.Mock).mockReturnValue(mockNavigate);
    });

    it("renders form elements", () => {
        render(
            <MemoryRouter>
                <LoginForm />
            </MemoryRouter>
        );

        expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
        expect(screen.getByText(/login/i)).toBeInTheDocument();
        expect(screen.getByText(/register/i)).toBeInTheDocument();
    });

    it("shows an error if fields are empty on submit", () => {
        render(
            <MemoryRouter>
                <LoginForm />
            </MemoryRouter>
        );

        const loginButton = screen.getByText(/login/i);
        fireEvent.click(loginButton);

        expect(screen.getByText(/please fill in all fields/i)).toBeInTheDocument();
    });

    it("navigates to the register page when Register button is clicked", () => {
        render(
            <MemoryRouter>
                <LoginForm />
            </MemoryRouter>
        );

        const registerButton = screen.getByText(/register/i);
        fireEvent.click(registerButton);

        expect(mockNavigate).toHaveBeenCalledWith("/register");
    });

    it("submits form and navigates based on role", async () => {
        mockedAxios.post.mockResolvedValueOnce({
            data: { role: "admin" },
        });

        render(
            <MemoryRouter>
                <LoginForm />
            </MemoryRouter>
        );

        const emailInput = screen.getByLabelText(/email/i);
        const passwordInput = screen.getByLabelText(/password/i);
        const loginButton = screen.getByText(/login/i);

        fireEvent.change(emailInput, { target: { value: "admin@example.com" } });
        fireEvent.change(passwordInput, { target: { value: "password123" } });
        fireEvent.click(loginButton);

        await waitFor(() => {
            expect(mockedAxios.post).toHaveBeenCalledWith(
                "http://localhost:8000/api/register",
                { email: "admin@example.com", password: "password123" }
            );
            expect(localStorage.getItem("user_role")).toBe("admin");
            expect(mockNavigate).toHaveBeenCalledWith("/admin");
        });
    });

    it("shows an error if login fails", async () => {
        mockedAxios.post.mockRejectedValueOnce(new Error("Invalid email or password"));

        render(
            <MemoryRouter>
                <LoginForm />
            </MemoryRouter>
        );

        const emailInput = screen.getByLabelText(/email/i);
        const passwordInput = screen.getByLabelText(/password/i);
        const loginButton = screen.getByText(/login/i);

        fireEvent.change(emailInput, { target: { value: "invalid@example.com" } });
        fireEvent.change(passwordInput, { target: { value: "wrongpassword" } });
        fireEvent.click(loginButton);

        await waitFor(() => {
            expect(screen.getByText(/invalid email or password/i)).toBeInTheDocument();
        });
    });
});
