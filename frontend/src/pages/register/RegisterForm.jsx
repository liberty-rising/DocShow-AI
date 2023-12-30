import React, { useState } from "react";
import { Alert, Box, Button, Checkbox, FormControlLabel, TextField, Typography } from "@mui/material";

function RegisterForm({ onSubmit, errorMessage }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [subscribe, setSubscribe] = useState(true);
    const [marketingContent, setMarketingContent] = useState(true); // New state variable

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        await onSubmit(username, email, password, subscribe, marketingContent, marketingContent); // Include new state variable in submission
    };
  
    return (
        <Box component="form" onSubmit={handleFormSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
                margin="normal"
                required
                fullWidth
                id="password"
                label="Password"
                name="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <FormControlLabel
                control={<Checkbox value="subscribe" color="primary" />}
                label="I want to receive updates by email."
                checked={subscribe}
                onChange={(e) => setSubscribe(e.target.checked)}
            />
            <FormControlLabel
                control={<Checkbox value="marketingContent" color="primary" />}
                label="I want to receive marketing content."
                checked={marketingContent}
                onChange={(e) => setMarketingContent(e.target.checked)}
            />
            <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
            >
                Sign Up
            </Button>
            {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
        </Box>
    );
}

export default RegisterForm;