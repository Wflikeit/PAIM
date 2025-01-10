import React from "react";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { configureStore } from "@reduxjs/toolkit";
import Sidebar from "../../../src/components/layout/Sidebar";

describe("Sidebar", () => {
  it("renders CheckBoxGroups for filters", () => {
    const store = configureStore({
      reducer: {
        products: () => ({
          filters: {
            fruitOrVegetable: [],
            countryOfOrigin: [],
          },
        }),
      },
    });

    render(
      <Provider store={store}>
        <BrowserRouter>
          <Sidebar />
        </BrowserRouter>
      </Provider>,
    );

    expect(screen.getByText("Category")).toBeInTheDocument();
    expect(screen.getByText("Country of origin")).toBeInTheDocument();
  });
});