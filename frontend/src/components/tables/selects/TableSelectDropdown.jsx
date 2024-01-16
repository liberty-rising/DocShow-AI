import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

function TableSelectDropdown({ tables, selectedTable, onTableSelect }) {
  const handleChange = (event) => {
    onTableSelect(event.target.value); // Update the parent component's state
  };

  return (
    <FormControl fullWidth margin="normal">
      <InputLabel id="table-select-label">Select Table</InputLabel>
      <Select
        labelId="table-select-label"
        id="table-select"
        value={selectedTable}
        label="Select Table"
        onChange={handleChange}
      >
        {tables.map((table) => (
          <MenuItem key={table} value={table}>
            {table}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

export default TableSelectDropdown;
