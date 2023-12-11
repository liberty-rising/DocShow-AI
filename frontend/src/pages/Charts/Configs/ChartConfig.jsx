import React, { useState, useEffect } from "react";
import { Box, Typography, CircularProgress } from "@mui/material";
import axios from 'axios';
import TableSelector from "./Components/TableSelector";
import ChartTypeSelector from "./Components/ChartTypeSelector";
import ChartPreview from "./Components/ChartPreview";
import { API_URL } from "../../../utils/constants";

function ChartConfig({ onConfigChange, onRequiredSelected, chartConfig, isLoading }) {
    const [tables, setTables] = useState([]);
    const [selectedTable, setSelectedTable] = useState('');
    const [chartTypes, setChartTypes] = useState([]);
    const [selectedChartType, setSelectedChartType] = useState('');
    const [organizationId, setOrganizationId] = useState(null);

    useEffect(() => {
        // Fetch user data from API
        axios.get(`${API_URL}users/me/`)
            .then(response => {
                // Set organizationId state
                setOrganizationId(response.data.organization_id);
    
                // Fetch tables from API using organizationId
                axios.get(`${API_URL}organization/${response.data.organization_id}/tables/`)
                    .then(response => setTables(response.data))
                    .catch(error => console.error('Error fetching tables:', error));
            })
            .catch(error => console.error('Error fetching user data:', error));
    }, []);

    useEffect(() => {
        // Fetch chart types from API
        axios.get(`${API_URL}charts/types/`)
            .then(response => setChartTypes(response.data))
            .catch(error => console.error('Error fetching chart types:', error));
    }, []); // Empty dependency array means this effect runs once on mount

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
        // Check if chartConfig.nivoConfig exists and is not an empty object
        return chartConfig.nivoConfig && Object.keys(chartConfig.nivoConfig).length > 0;
    };

    const handleTableChange = (event) => {
        const selectedTable = event.target.value;
        setSelectedTable(selectedTable);
    }

    const handleChartTypeChange = (event) => {
        const selectedType = event.target.value;
        setSelectedChartType(selectedType);
    };

    return(
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 120, marginBottom: 2, width: '100%' }}>
            <TableSelector selectedTable={selectedTable} onTableChange={handleTableChange} tables={tables} />
            <ChartTypeSelector selectedChartType={selectedChartType} onChartTypeChange={handleChartTypeChange} chartTypes={chartTypes} />
            {isLoading ? (
                <CircularProgress />
            ) : (
                canShowPreview() ? (
                    <ChartPreview chartConfig={chartConfig} />
                ) : (
                    <Typography variant="caption">Configure the chart to preview it here.</Typography>
                )
            )}
        </Box>
    )
}

export default ChartConfig