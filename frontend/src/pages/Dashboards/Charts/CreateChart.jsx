import React, { useState, useEffect } from "react";
import { Box, Button, capitalize, FormControl, InputLabel, MenuItem, Paper, Select, Typography } from "@mui/material";
import axios from 'axios';
import { useNavigate, useParams } from "react-router-dom";
import ChartSettings from "./Settings/ChartSettings";
import { API_URL } from "../../../utils/constants";

const CreateChartPage = () => {
    const [tables, setTables] = useState([]);
    const [selectedTable, setSelectedTable] = useState('');
    const [chartTypes, setChartTypes] = useState([]);
    const [selectedChartType, setSelectedChartType] = useState('');
    const [chartConfig, setChartConfig] = useState({});
    const { dashboardId } = useParams(); // Retrieve the dashboardId from the URL parameter
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch tables from API
        axios.get(`${API_URL}tables/`)
            .then(response => setTables(response.data))
            .catch(error => console.error('Error fetching tables:', error))

        // Fetch chart types from API
        axios.get(`${API_URL}charts/types/`)
            .then(response => setChartTypes(response.data))
            .catch(error => console.error('Error fetching chart types:', error));
    }, []);

    const handleTableChange = (event) => {
        const selectedTable = event.target.value;
        setSelectedTable(selectedTable);
    }

    const handleChartTypeChange = (event) => {
        const selectedType = event.target.value;
        setSelectedChartType(selectedType);
        // Reset chart config when chart type changes
        setChartConfig({});
    };

    const handleSubmit = () => {
        // Logic to handle form submission
        console.log("Creating chart with type:", selectedChartType, "and config:", chartConfig);
    };

    const handleBack = () => {
        navigate(`/dashboards/${dashboardId}`)
    }

    return (
        <Paper elevation={3} sx={{ padding: 3, margin: 3, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '80%', maxWidth: '600px' }}>
            <Typography variant="h6" gutterBottom>Create a Chart:</Typography>
            <Box sx={{ minWidth: 120, marginBottom: 2, width: '100%' }}>
                <FormControl fullWidth margin="normal">
                    <InputLabel id="table-select-label">Table</InputLabel>
                    <Select 
                        labelId="table-select-label" 
                        id="table-select"
                        value={selectedTable}
                        label="Table"
                        onChange={handleTableChange}
                    >
                        {tables.map((table) => (
                            <MenuItem key={table} value={table}>{table}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl fullWidth margin="normal" disabled={!selectedTable}>
                    <InputLabel id="chart-type-select-label">Chart Type</InputLabel>
                    <Select
                        labelId="chart-type-select-label"
                        id="chart-type-select"
                        value={selectedChartType}
                        label="Chart Type"
                        onChange={handleChartTypeChange}
                    >
                        {chartTypes.map((type) => (
                            <MenuItem key={type.name} value={type.name}>{capitalize(type.name)}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>
            <ChartSettings selectedChartType={selectedChartType} />
            <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', width: '100%', mt: 2 }}>
                <Button variant="contained" onClick={handleSubmit} sx={{ mb: 2 }}>
                    Create Chart
                </Button>
                <Button variant="outlined" onClick={handleBack}>
                    Back to Dashboard
                </Button>
            </Box>
        </Paper>
    );
};


export default CreateChartPage;
