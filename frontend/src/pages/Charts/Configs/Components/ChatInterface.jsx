import React, { useState } from "react";
import { Box, TextField, Button, Paper } from "@mui/material";

function ChatInterface({ onSendRequest, disabled }) {
    const [message, setMessage] = useState('');

    const handleSubmit = () => {
        if (message.trim()) {
            onSendRequest(message);
            setMessage('');
        }
    };

    return (
        <Paper elevation={3} sx={{ padding: 2, margin: 2, width: "80%" }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TextField
                    fullWidth
                    disabled={disabled}
                    variant="outlined"
                    placeholder="Ask the LLM to configure the chart..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                />
                <Button variant="contained" onClick={handleSubmit} disabled={disabled}>
                    Send
                </Button>
            </Box>
        </Paper>
    );
}

export default ChatInterface;
