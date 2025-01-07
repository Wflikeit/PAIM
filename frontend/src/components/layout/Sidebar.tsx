import React from "react";
import List from "@mui/material/List";
import { Box } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { RootState } from "../../redux/store";
import CheckBoxGroup from "./CheckBoxGroup";
import {
  setCountryOfOriginFilter,
  setFruitOrVegetableFilter,
} from "../../model/product";

const Sidebar: React.FC = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const { filters } = useSelector((state: RootState) => state.products);

  // Only render the sidebar on the root path
  if (location.pathname !== "/") {
    return null;
  }

  // Define filter categories with explicit typing for filterKey
  const categories: {
    title: string;
    options: string[];
    filterValues: string[];
    filterKey: keyof typeof filters; // Ensure filterKey matches filters keys
    filterAction: (value: string) => any;
  }[] = [
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
        <List sx={{ position: "sticky", top: "0", marginBottom: "200px" }}>
          <Box sx={{ mt: 1, color: "#4caf50" }}>
            {categories.map((category, index) => (
                <CheckBoxGroup
                    key={index}
                    title={category.title}
                    options={category.options}
                    filterValues={category.filterValues}
                    selectedValues={filters[category.filterKey] || []} // Pass selected filter values
                    onChange={(filterValue: string) => {
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
