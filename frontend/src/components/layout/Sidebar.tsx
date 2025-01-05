import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import {
  Box,
  Checkbox,
  FormControlLabel,
  Input,
  Slider,
  Stack,
} from "@mui/material";
import { blue } from "@mui/material/colors";
import { useDispatch, useSelector } from "react-redux";

import { useLocation } from "react-router-dom";
import { RootState } from "../../redux/store.ts";
import { applyFilter, setFruitOrVegetableFilter } from "../../model/product.ts";

const Sidebar = () => {
  const location = useLocation();
  const [value, setValue] = React.useState(30);

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setValue(newValue as number);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value === "" ? 0 : Number(event.target.value));
  };
  const dispatch = useDispatch();
  const { filters } = useSelector((state: RootState) => state.products);

  const handleCheckboxChange = (value: string | null) => {
    const newValue = filters.fruitOrVegetable === value ? null : value; // Toggle filter
    dispatch(setFruitOrVegetableFilter(newValue));
    dispatch(applyFilter());
  };

  const categories = [
    {
      title: "Category",
      options: ["Warzywa", "Owoce"],
    },
    {
      title: "Kraj pochodzenia",
      options: ["Polska", "Hiszpania"],
    },
  ];

  const handleBlur = () => {
    if (value < 0) {
      setValue(0);
    } else if (value > 100) {
      setValue(100);
    }
  };

  if (location.pathname !== "/") {
    return null;
  }

  return (
    <nav className="sidebar">
      <List style={{ position: "sticky", marginBottom: "200px" }}>
        <Box sx={{ mt: 1, color: blue[500] }}>
          <ListItem>
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.fruitOrVegetable === "Warzywa"}
                  onChange={() => handleCheckboxChange("Warzywo")}
                />
              }
              label="Warzywa"
            />
          </ListItem>
          <ListItem>
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.fruitOrVegetable === "Owoc"}
                  onChange={() => handleCheckboxChange("Owoc")}
                />
              }
              label="Owoce"
            />
          </ListItem>
          <ListItem>
            <Box style={{ color: blue[500], width: "100%" }}>
              <h3>Max Price</h3>
              <Stack direction="column" spacing={2} alignItems="center">
                <Slider
                  value={typeof value === "number" ? value : 0}
                  onChange={handleSliderChange}
                  aria-labelledby="input-slider"
                  sx={{ flex: 1 }}
                />
                <div>
                  <Input
                    value={value}
                    size="small"
                    onChange={handleInputChange}
                    onBlur={handleBlur}
                    inputProps={{
                      step: 10,
                      min: 0,
                      max: 100,
                      type: "number",
                      "aria-labelledby": "input-slider",
                    }}
                    sx={{ width: "50%" }}
                  />
                  <span style={{ marginLeft: "10px" }}>Zł</span>
                </div>
              </Stack>
            </Box>
          </ListItem>
        </Box>
      </List>
    </nav>
  );
};

export default Sidebar;