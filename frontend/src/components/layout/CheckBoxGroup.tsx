import React from "react";
import { Box, Checkbox, FormControlLabel, Typography } from "@mui/material";

interface CheckboxGroupProps {
    title: string;
    options: string[];
}

const CheckboxGroup: React.FC<CheckboxGroupProps> = ({ title, options }) => {
    return (
        <Box sx={{ display: "flex", flexDirection: "column", mb: 2, alignItems: "center" }}>
            <Typography variant="h6" sx={{ mb: 1, textAlign: "center" }}>
                {title}
            </Typography>
            <Box sx={{ display: "flex", gap: 2, justifyContent: "center" }}>
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