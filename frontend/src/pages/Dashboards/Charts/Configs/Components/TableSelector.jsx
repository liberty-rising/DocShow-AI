import React from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

function TableSelector({ selectedTable, onTableChange, tables }) {
    return (
        <FormControl fullWidth margin="normal">
            <InputLabel id="table-select-label">Table</InputLabel>
            <Select 
                labelId="table-select-label" 
                id="table-select"
                value={selectedTable}
                label="Table"
                onChange={onTableChange}
            >
                {tables.map((table) => (
                    <MenuItem key={table} value={table}>{table}</MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}

export default TableSelector