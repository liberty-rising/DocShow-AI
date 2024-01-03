import React from "react";
import { capitalize, FormControl, InputLabel, MenuItem, Select } from "@mui/material";

function ChartTypeSelector({ selectedChartType, onChartTypeChange, chartTypes }) {
    return (
        <FormControl fullWidth margin="normal">
            <InputLabel id="chart-type-select-label">Chart Type</InputLabel>
            <Select
                labelId="chart-type-select-label"
                id="chart-type-select"
                value={selectedChartType}
                label="Chart Type"
                onChange={onChartTypeChange}
            >
                {chartTypes.map((type) => (
                    <MenuItem key={type.name} value={type.name}>{capitalize(type.name)}</MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}

export default ChartTypeSelector