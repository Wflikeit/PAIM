import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "react-query";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import Admin from "../../src/pages/Admin"; // Adjust the path if necessary

// Mock Chart.js to avoid rendering actual charts during tests
jest.mock("react-chartjs-2", () => ({
    Bar: () => <div data-testid="mock-bar-chart">Mocked Bar Chart</div>,
}));

const queryClient = new QueryClient();

describe("Admin Component", () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test("renders the Admin component with expected elements", () => {
        render(
            <QueryClientProvider client={queryClient}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <Admin />
                </LocalizationProvider>
            </QueryClientProvider>
        );

        // Check for the header
        expect(screen.getByText(/Admin Panel - Reports/i)).toBeInTheDocument();

        // Check for the date pickers
        expect(screen.getByLabelText(/Start Date/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/End Date/i)).toBeInTheDocument();

        // Check for the Generate Report button
        expect(screen.getByRole("button", { name: /Generate Report/i })).toBeInTheDocument();

        // Check for the mock bar charts
        const barCharts = screen.getAllByTestId("mock-bar-chart");
        expect(barCharts).toHaveLength(2);

        // Check for the table headers (use `getAllByText` for duplicate elements)
        const tableHeaders = screen.getAllByText(/Number of Transports/i);
        expect(tableHeaders).toHaveLength(2); // One in table header, one in chart title

        expect(screen.getByText(/Destination Region/i)).toBeInTheDocument();
        expect(screen.getByText(/Destination District/i)).toBeInTheDocument();
    });

    test("allows selecting dates and clicking the Generate Report button", () => {
        render(
            <QueryClientProvider client={queryClient}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <Admin />
                </LocalizationProvider>
            </QueryClientProvider>
        );

        // Mock the date pickers interaction
        const startDateInput = screen.getByLabelText(/Start Date/i);
        const endDateInput = screen.getByLabelText(/End Date/i);

        fireEvent.change(startDateInput, { target: { value: "01/01/2023" } });
        fireEvent.change(endDateInput, { target: { value: "12/31/2023" } });

        // Simulate button click
        const generateReportButton = screen.getByRole("button", { name: /Generate Report/i });
        fireEvent.click(generateReportButton);

        // Verify that the button is enabled and clicked
        expect(generateReportButton).toBeEnabled();
    });
});
