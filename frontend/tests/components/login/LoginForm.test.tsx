import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import axios from "axios";
import LoginForm from "../../../src/components/login/LoginForm";
import {MemoryRouter} from "react-router-dom";

jest.mock("axios");

describe("LoginForm", () => {
  it("submits form and navigates based on role", async () => {
    // Mock FormData and append behavior
    const mockFormData = new FormData();
    mockFormData.append("username", "admin@example.com");
    mockFormData.append("password", "password123");

    // Mock axios.post
    (axios.post as jest.Mock).mockResolvedValueOnce({
      data: {
        access_token: `header.${btoa(
          JSON.stringify({ role: "admin" })
        )}.signature`,
        fullname: "Admin User",
      },
    });

    render(
        <MemoryRouter>
          <LoginForm />);
        </MemoryRouter>

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "admin@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      // Check that axios.post was called with the correct arguments
      expect(axios.post).toHaveBeenCalledWith(
        "http://127.0.0.1:8002/auth/login",
        expect.any(FormData), // Check that FormData is passed
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      // Verify localStorage values
      expect(localStorage.getItem("access_token")).toBe(
        "header.eyJyb2xlIjoiYWRtaW4ifQ==.signature"
      );
      expect(localStorage.getItem("user_role")).toBe("admin");
    });
  });

  it("shows error message on invalid credentials", async () => {
    // Mock axios.post rejection
    (axios.post as jest.Mock).mockRejectedValueOnce(new Error("Invalid email or password"));

    render(<LoginForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "wrong@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "wrongpassword" },
    });

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      // Check that error message is displayed
      expect(screen.getByText(/invalid email or password/i)).toBeInTheDocument();
    });

    // Ensure axios.post was called
    expect(axios.post).toHaveBeenCalledWith(
      "http://127.0.0.1:8002/auth/login",
      expect.any(FormData),
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }
    );
  });
});
