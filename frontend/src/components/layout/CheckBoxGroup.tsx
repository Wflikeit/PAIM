import React from "react";
import { Box, Checkbox, FormControlLabel, Typography } from "@mui/material";

interface CheckboxGroupProps {
  title: string;
  options: string[];
}

const CheckboxGroup: React.FC<CheckboxGroupProps> = ({ title, options }) => {
    return (
        <Box sx={{ mb: 2, marginLeft:"1rem" }}>
            <Typography variant="h6" sx={{ mb: 1 }}>
                {title}
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {options.map((option, index) => (
                    <FormControlLabel
                        key={index}
                        control={<Checkbox />}
                        label={option}
                        sx={{ display: 'inline-flex', alignItems: 'center' }}
                    />
                ))}
            </Box>
        </Box>
    );
};
export default CheckboxGroup;