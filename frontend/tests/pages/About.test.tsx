import { render, screen } from "@testing-library/react";
import About from "../../src/pages/About";

describe("About", () => {
    it("renders the About page", () => {
        render(<About />);

        // Check for the heading
        expect(screen.getByText(/O nas/i)).toBeInTheDocument();

        // Check for the paragraph text
        expect(
            screen.getByText(/Welcome to our website! We are a company that strives for perfection in every aspect./i)
        ).toBeInTheDocument();
    });
});
