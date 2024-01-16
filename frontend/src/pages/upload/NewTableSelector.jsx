import React from "react";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
} from "@mui/material";

const NewTableSelector = ({ isNewTable, setIsNewTable }) => (
  <FormControl component="fieldset">
    <FormLabel component="legend">Is a new table needed?</FormLabel>
    <RadioGroup
      row
      value={isNewTable}
      onChange={(e) => setIsNewTable(e.target.value)}
    >
      <FormControlLabel value="yes" control={<Radio />} label="Yes" />
      <FormControlLabel value="no" control={<Radio />} label="No" />
    </RadioGroup>
  </FormControl>
);

export default NewTableSelector;
