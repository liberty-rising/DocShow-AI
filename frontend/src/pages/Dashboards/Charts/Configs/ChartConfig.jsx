import React, { useState, useEffect } from "react";
import { Box, Typography } from "@mui/material";
import axios from 'axios';
import TableSelector from "./Components/TableSelector";
import ChartTypeSelector from "./Components/ChartTypeSelector";
// import ChartConfigForm from "./Components/ChartConfigForm";
import ChartPreview from "./Components/ChartPreview";
import { API_URL } from "../../../../utils/constants";

function ChartConfig({ onConfigChange, onRequiredSelected }) {
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

    useEffect(() => {
        onConfigChange({
            table: selectedTable,
            type: selectedChartType
        })
    })

    const updateRequiredSelected = () => {
        // Ensure chat with LLM is only possible when required selects are selected
        const requiredSelected = selectedTable && selectedChartType;
        onRequiredSelected(requiredSelected);
    }

    useEffect(() => {
        updateRequiredSelected();
    }, [selectedTable, selectedChartType])

    const canShowPreview = () => {
        // Example condition for a bar chart: Check if table and chart type are selected
        // and specific config for the chart type is set
        return selectedTable && selectedChartType
    };

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

    // const handleChartSpecificConfigChange = (config) => {
    //     setChartSpecificConfig(config);
    //     // Update the overall configuration
    //     const overallConfig = {
    //         type: selectedChartType,
    //         config: config,
    //         table: selectedTable
    //     };
    //     onConfigChange(overallConfig);
    // };

    return(
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 120, marginBottom: 2, width: '100%' }}>
            <TableSelector selectedTable={selectedTable} onTableChange={handleTableChange} tables={tables} />
            <ChartTypeSelector selectedChartType={selectedChartType} onChartTypeChange={handleChartTypeChange} chartTypes={chartTypes} />
            {/* <ChartConfigForm selectedTable={selectedTable} selectedChartType={selectedChartType} onConfigChange={handleChartSpecificConfigChange} /> */}
            {canShowPreview() ? (
                <ChartPreview chartConfig={chartSpecificConfig} />
            ) : (
                <Typography variant="caption">Select the required options to preview the chart.</Typography>
            )}
            
        </Box>
    )
}

export default ChartConfig