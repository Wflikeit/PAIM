import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import {
  Box,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  FormLabel,
  Grid,
  Input,
  Slider,
} from "@mui/material";
import { blue } from "@mui/material/colors";
import { Money } from "@mui/icons-material";

const Sidebar = () => {
  const resolveLinkClass = ({ isActive }: { isActive: boolean }): string => {
    return isActive ? "link link__active" : "link";
  };

  const [value, setValue] = React.useState(30);

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setValue(newValue as number);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value === "" ? 0 : Number(event.target.value));
  };

  const handleBlur = () => {
    if (value < 0) {
      setValue(0);
    } else if (value > 100) {
      setValue(100);
    }
  };

  return (
    <nav className="sidebar">
      <List style={{ position: "sticky", top: "45px" }}>
        <Box sx={{ mt: 1 }}>
          <ListItem sx={{ display: "grid", placeContent: "center" }}>
            <Box style={{ color: blue[500] }}>
              <FormControl
                sx={{ m: 3 }}
                component="fieldset"
                variant="standard"
              >
                <FormLabel>Category</FormLabel>
                <FormGroup>
                  <FormControlLabel
                    control={<Checkbox></Checkbox>}
                    label="Warzywa"
                  />
                  <FormControlLabel
                    control={<Checkbox></Checkbox>}
                    label="Owoce"
                  />
                </FormGroup>
              </FormControl>
            </Box>
          </ListItem>

          <ListItem sx={{ display: "grid", placeContent: "center" }}>
            <Box style={{ color: blue[500] }}>
              <FormControl
                sx={{ m: 3 }}
                component="fieldset"
                variant="standard"
              >
                <FormLabel>Kraj pochodzenia</FormLabel>
                <FormGroup>
                  <FormControlLabel
                    control={<Checkbox></Checkbox>}
                    label="Polska"
                  />
                  <FormControlLabel
                    control={<Checkbox></Checkbox>}
                    label="Hiszpania"
                  />
                </FormGroup>
              </FormControl>
            </Box>
          </ListItem>
          <ListItem>
            <Box style={{ color: blue[500] }}>
              <Grid container spacing={2} sx={{ alignItems: "center" }}>
                <Grid item>
                  <Money />
                </Grid>
                <Grid item xs>
                  <Slider
                    value={typeof value === "number" ? value : 0}
                    onChange={handleSliderChange}
                    aria-labelledby="input-slider"
                  />
                </Grid>
                <Grid item>
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
                  />
                </Grid>
              </Grid>
            </Box>
          </ListItem>
        </Box>
      </List>
    </nav>
  );
};

export default Sidebar;