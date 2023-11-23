import React, { useState } from "react";
import { Box, Button, Paper, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import ChartConfig from "./Configs/ChartConfig";

const CreateChartPage = () => {
    const { dashboardId } = useParams(); // Retrieve the dashboardId from the URL parameter
    const navigate = useNavigate();
    const [chartConfig, setChartConfig] = useState({ type: '', settings: {} });

    const handleChartConfigChange = (config) => {
        setChartConfig(config);
    };

    const handleSubmit = () => {
        // Logic to handle form submission
        console.log("Creating chart with config:", chartConfig);
        // Post chartConfig to your database
    };

    const handleBack = () => {
        navigate(`/dashboards/${dashboardId}`)
    }

    return (
        <Paper elevation={3} sx={{ padding: 3, margin: 3, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '80%', maxWidth: '600px' }}>
            <Typography variant="h6" gutterBottom>Create a Chart:</Typography>
            <ChartConfig onConfigChange={handleChartConfigChange} />
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
