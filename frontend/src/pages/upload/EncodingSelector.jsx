import React from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

const EncodingSelector = ({ encodings, encoding, setEncoding }) => (
  <FormControl fullWidth>
    <InputLabel id="encoding-label">Choose an encoding</InputLabel>
    <Select
      labelId="encoding-label"
      value={encoding}
      label="Choose an encoding"
      onChange={(e) => setEncoding(e.target.value)}
    >
      {encodings.map((enc, index) => (
        <MenuItem key={index} value={enc}>
          {enc.toUpperCase()}
        </MenuItem>
      ))}
    </Select>
  </FormControl>
);

export default EncodingSelector;
