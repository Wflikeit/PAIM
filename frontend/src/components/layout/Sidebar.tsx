import React from "react";
import List from "@mui/material/List";
import { Box } from "@mui/material";
import { blue } from "@mui/material/colors";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { RootState } from "../../redux/store";
import CheckBoxGroup from "./CheckBoxGroup";
import {
  setCountryOfOriginFilter,
  setFruitOrVegetableFilter,
} from "../../model/product";

const Sidebar = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const { filters } = useSelector((state: RootState) => state.products);

  if (location.pathname !== "/") {
    return null;
  }

  // Define filter categories
  const categories = [
    {
      title: "Category",
      options: ["Warzywa", "Owoce"], // Displayed labels
      filterValues: ["Warzywo", "Owoc"], // Actual filter values
      filterKey: "fruitOrVegetable", // Corresponding key in Redux state
      filterAction: setFruitOrVegetableFilter, // Redux action to update the filter
    },
    {
      title: "Kraj pochodzenia",
      options: ["Polska", "Hiszpania"],
      filterValues: ["Polska", "Hiszpania"],
      filterKey: "countryOfOrigin",
      filterAction: setCountryOfOriginFilter,
    },
  ];

  return (
    <nav className="sidebar">
      <List style={{ position: "sticky", marginBottom: "200px" }}>
        <Box sx={{ mt: 1, color: blue[500] }}>
          {/* Render CheckBoxGroup dynamically for each category */}
          {categories.map((category, index) => (
            <CheckBoxGroup
              key={index}
              title={category.title}
              options={category.options}
              filterValues={category.filterValues}
              selectedValues={filters[category.filterKey] || []} // Pass selected filter values
              onChange={(filterValue: string) => {
                // Dispatch the appropriate filter action
                dispatch(category.filterAction(filterValue));
              }}
            />
          ))}
        </Box>
      </List>
    </nav>
  );
};

export default Sidebar;