import React, { useState } from "react";
import { Box, TextField, Button, Paper, CircularProgress } from "@mui/material";

function ChatInterface({ onSendRequest, disabled }) {
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    
    const handleSubmit = async () => {
        if (message.trim()) { // Checks if the message is not empty after trimming whitespace
            setIsLoading(true); // Sets the loading state to true
            await onSendRequest(message); // Sends the request with the message
            setMessage(''); // Clears the message
            setIsLoading(false); // Sets the loading state to false
        }
    };

    return (
        <Paper elevation={3} sx={{ padding: 2, margin: 2, width: "80%" }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TextField
                    fullWidth
                    disabled={disabled || isLoading}
                    variant="outlined"
                    placeholder="Ask the LLM to configure the chart..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                />
                <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={disabled || isLoading}
                    startIcon={isLoading ? <CircularProgress size={20} /> : null}
                >
                    Send
                </Button>
            </Box>
        </Paper>
    );
}

export default ChatInterface;
