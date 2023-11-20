import React from "react";
import { TextField } from "@mui/material";

const DescriptionField = ({ description, setDescription }) => (
    <TextField
        label="Add a description (optional)"
        fullWidth
        margin="normal"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
    />
)

export default DescriptionField;