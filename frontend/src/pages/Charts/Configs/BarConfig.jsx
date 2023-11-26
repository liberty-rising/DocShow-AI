import React, { useEffect, useState } from "react";
import { Box, Button, Collapse, FormControl, InputLabel, MenuItem, Select, Typography } from "@mui/material";
import axios from "axios";
import { API_URL } from "../../../utils/constants";

function BarConfig({ selectedTable, onBarConfigChange }) {
    const [columns, setColumns] = useState([]);
    const [selectedIndexBy, setSelectedIndexBy] = useState('');  // In a simple bar chart, this will be the x-axis
    const [selectedKeys, setSelectedKeys] = useState('');  // In a simple bar chart, this will be the y-axis
    const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);

    useEffect(() => {
        if (selectedTable) {
            axios.get(`${API_URL}table/columns/?table_name=${selectedTable}`) // Use the table name in the API call
                .then(response => setColumns(response.data))
                .catch(error => console.error('Error fetching columns:', error));
        }
    }, [selectedTable]);

    useEffect(() => {
        // Whenever selectedIndexBy or selectedKeys changes, call onBarConfigChange
        onBarConfigChange({
            indexBy: selectedIndexBy,
            keys: selectedKeys
        });
    }, [selectedIndexBy, selectedKeys, onBarConfigChange]);

    const handleIndexChange = (event) => {
        setSelectedIndexBy(event.target.value);
    }
    
    const handleKeysChange = (event) => {
        setSelectedKeys(event.target.value);
    }

    const handleToggleAdvancedSettings = () => {
        setShowAdvancedSettings(!showAdvancedSettings);
    }

    const AdvancedSettings = () => (
        <Box>
            {/* Implement your advanced settings here */}
            <Typography>Advanced settings...</Typography>
        </Box>
    );

    // Prevents users from selecting the same column twice
    const getFilteredColumnsForAxis = (axisType) => {  
        return columns.filter(column => {
            if (axisType === 'xAxis') {
                return column !== selectedKeys;
            } else { // yAxis
                return column !== selectedIndexBy;
            }
        });
    };

    return (
        <Box>
            <Box sx={{ display: 'flex', flexDirection: 'row' }}>
                <FormControl fullWidth margin="normal">
                    <InputLabel id="x-axis-select-label">X-Axis: Categories</InputLabel>
                    <Select
                        labelId="x-axis-select-label"
                        id="x-axis-select"
                        value={selectedIndexBy}
                        label="X-Axis: Categories"
                        onChange={handleIndexChange}
                        placeholder="Select column for bar categories/groups"
                    >
                        <MenuItem value="">---</MenuItem> {/* Option to select nothing */}
                        {getFilteredColumnsForAxis('xAxis').map((column) => (
                            <MenuItem key={column} value={column}>{column}</MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl fullWidth margin="normal">
                    <InputLabel id="y-axis-select-label">Y-Axis: Values</InputLabel>
                    <Select
                        labelId="y-axis-select-label"
                        id="y-axis-select"
                        value={selectedKeys}
                        label="Y-Axis: Values"
                        onChange={handleKeysChange}
                        // placeholder="Select column for bar values"
                    >
                        <MenuItem value="">---</MenuItem> {/* Option to select nothing */}
                        {getFilteredColumnsForAxis('yAxis').map((column) => (
                            <MenuItem key={column} value={column}>{column}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>

            {/* Advanced Settings Toggle */}
            <Button onClick={handleToggleAdvancedSettings}>
                {showAdvancedSettings ? "Hide Advanced Settings" : "Show Advanced Settings"}
            </Button>

            {/* Advanced Settings Section */}
            <Collapse in={showAdvancedSettings}>
                <AdvancedSettings />
            </Collapse>
        </Box>
    )
}

export default BarConfig