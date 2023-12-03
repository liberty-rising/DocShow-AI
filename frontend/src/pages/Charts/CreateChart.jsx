import React, { useEffect, useState } from "react";
import { Box, Button, Paper, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import ChartConfig from "./Configs/ChartConfig";
import ChatInterface from "./Configs/Components/ChatInterface";
import { API_URL } from "../../utils/constants";

const CreateChartPage = () => {
    const { dashboardId } = useParams(); // Retrieve the dashboardId from the URL parameter
    const navigate = useNavigate();
    const [chartConfig, setChartConfig] = useState({ title: '', table: '', type: '', query: '', nivoConfig: {} });
    const [isChatEnabled, setIsChatEnabled] = useState(false);
    const [chartChatId, setChartChatId] = useState(null);

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

            // Setting a longer timeout, e.g., 30 seconds (30000 milliseconds)
            const axiosConfig = {
                timeout: 120000 // TODO: 120 seconds, this is quite long, try to shorten it
            };

            const response = await axios.post(`${API_URL}chart/config/`, {
                chat_id: chartChatId,
                msg: message,  // message to the llm
                chart_config: configToSend
            }, axiosConfig);

            const updatedChartConfig = response.data[0];
            setChartConfig(updatedChartConfig);

            // Update chatChatId with the new chat_id from the response
            if (response.data[0] && response.data[1]) {
                setChartChatId(response.data[1]);
            }
        } catch (error) {
            console.error("Error communicating with LLM:", error);
            // Enhanced error logging
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.error("Error Data:", error.response.data);
                console.error("Error Status:", error.response.status);
                console.error("Error Headers:", error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                console.error("Error Request:", error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.error("Error Message:", error.message);
            }
            console.error("Error Config:", error.config);
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        axios.post(`${API_URL}chart/`, { dashboard_id: dashboardId, config: chartConfig })
        .then(response => {
            // Handle successful dashboard creation
            console.log('Chart created:', response.data);
            navigate(`/dashboards/${dashboardId}`)
        })
        .catch(error => {
            console.error('Error creating dashboard:', error);
        });
    };

    const handleBack = () => {
        navigate(`/dashboards/${dashboardId}`)
    }

    return (
        <Paper elevation={3} sx={{ padding: 3, margin: 3, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '80%', maxWidth: '600px' }}>
            <Typography variant="h6" gutterBottom>Create a Chart:</Typography>
            <ChartConfig 
                onConfigChange={handleChartConfigChange} 
                onRequiredSelected={handleRequiredSelected} 
                chartConfig={chartConfig} 
            />
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
