import React, { useState } from "react";
import { Box, Button, Paper, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import ChartConfig from "./Configs/ChartConfig";
import ChatInterface from "./Configs/Components/ChatInterface";
import { API_URL } from "../../../utils/constants";

const CreateChartPage = () => {
    const { dashboardId } = useParams(); // Retrieve the dashboardId from the URL parameter
    const navigate = useNavigate();
    const [chartConfig, setChartConfig] = useState({ table: '', type: '', nivoConfig: {} });
    const [isChatEnabled, setIsChatEnabled] = useState(false);

    const handleChartConfigChange = (config) => {
        setChartConfig(prevConfig => ({ ...prevConfig, ...config }))
        setIsChatEnabled(true);
    };

    const handleRequiredSelected = (isChatEnabled) => {
        // Ensure chat with LLM is only possible when required selects are selected
        setIsChatEnabled(isChatEnabled);
    }
    
    const handleSendRequest = async (message) => {
        // Message to LLM
        try {
            // Ensure nivoConfig is set to an empty object if it doesn't exist
            const configToSend = {
                ...chartConfig,
                nivoConfig: chartConfig.nivoConfig || {}
            };

            const response = await axios.post(`${API_URL}chart/config/`, {
                msg: message,  // message to the llm
                chart_config: configToSend
            });

            const updatedChartConfig = response.data.json();
            setChartConfig(updatedChartConfig);
        } catch (error) {
            console.error("Error communicating with LLM:", error);
        }
    }

    console.log(chartConfig.nivoConfig)
    const handleSubmit = async () => {
    };

    const handleBack = () => {
        navigate(`/dashboards/${dashboardId}`)
    }

    return (
        <Paper elevation={3} sx={{ padding: 3, margin: 3, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '80%', maxWidth: '600px' }}>
            <Typography variant="h6" gutterBottom>Create a Chart:</Typography>
            <ChartConfig onConfigChange={handleChartConfigChange} onRequiredSelected={handleRequiredSelected} />
            <ChatInterface onSendRequest={handleSendRequest} disabled={!isChatEnabled} />
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
