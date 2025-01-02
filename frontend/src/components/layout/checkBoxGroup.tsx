import React from "react";
import { Box, Checkbox, FormControlLabel, Typography } from "@mui/material";

const CheckboxGroup = ({ title, options }) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        mb: 2,
        marginLeft: "18px",
      }}
    >
      <Typography variant="h6" sx={{ mb: 1 }}>
        {title}
      </Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {options.map((option, index) => (
          <FormControlLabel
            key={index}
            control={<Checkbox />}
            label={option}
            sx={{ display: "inline-flex", alignItems: "center" }}
          />
        ))}
      </Box>
    </Box>
  );
};
export default CheckboxGroup;