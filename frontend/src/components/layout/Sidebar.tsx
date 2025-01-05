import React from "react";
import List from "@mui/material/List";
import { Box } from "@mui/material";
import { blue } from "@mui/material/colors";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { RootState } from "../../redux/store";
import CheckBoxGroup from "./CheckBoxGroup";
import {
  applyFilter,
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

  const categories = [
    {
      title: "Category",
      options: ["Warzywa", "Owoce"],
      filterValues: ["Warzywo", "Owoc"],
      filterKey: "fruitOrVegetable",
      filterAction: setFruitOrVegetableFilter,
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
          {categories.map((category, index) => (
            <CheckBoxGroup
              key={index}
              title={category.title}
              options={category.options}
              filterValues={category.filterValues}
              selectedValues={filters[category.filterKey] || []}
              onChange={(filterValue: string) => {
                dispatch(category.filterAction(filterValue));
                dispatch(applyFilter());
              }}
            />
          ))}
        </Box>
      </List>
    </nav>
  );
};

export default Sidebar;