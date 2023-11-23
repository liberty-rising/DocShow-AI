import React, { useState, useEffect } from "react";
import { Box } from "@mui/material";
import axios from 'axios';
import TableSelector from "./Components/TableSelector";
import ChartTypeSelector from "./Components/ChartTypeSelector";
import ChartConfigForm from "./Components/ChartConfigForm";
import ChartPreview from "./Components/ChartPreview";
import { API_URL } from "../../../../utils/constants";

function ChartConfig({ onConfigChange }) {
    const [tables, setTables] = useState([]);
    const [selectedTable, setSelectedTable] = useState('');
    const [chartTypes, setChartTypes] = useState([]);
    const [selectedChartType, setSelectedChartType] = useState('');
    const [chartSpecificConfig, setChartSpecificConfig] = useState({});

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
        setChartSpecificConfig({});
    };

    const handleChartSpecificConfigChange = (config) => {
        setChartSpecificConfig(config);
        // Update the overall configuration
        const overallConfig = {
            type: selectedChartType,
            settings: config,
            table: selectedTable
        };
        onConfigChange(overallConfig);
    };

    return(
        <Box sx={{ minWidth: 120, marginBottom: 2, width: '100%' }}>
            <TableSelector selectedTable={selectedTable} onTableChange={handleTableChange} tables={tables} />
            <ChartTypeSelector selectedChartType={selectedChartType} onChartTypeChange={handleChartTypeChange} chartTypes={chartTypes} />
            <ChartConfigForm selectedTable={selectedTable} selectedChartType={selectedChartType} onConfigChange={handleChartSpecificConfigChange} />
            <ChartPreview chartConfig={chartSpecificConfig} />
        </Box>
    )
}

export default ChartConfig