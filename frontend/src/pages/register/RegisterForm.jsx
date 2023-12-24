import React, { useState } from "react";
import { Alert, Box, Button, Checkbox, FormControlLabel, TextField, Typography } from "@mui/material";

function RegisterForm({ onSubmit, errorMessage }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [subscribe, setSubscribe] = useState(false);

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        await onSubmit(username, email, password);
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
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <FormControlLabel
                control={<Checkbox value="subscribe" color="primary" />}
                label="I want to receive inspiration, marketing promotions and updates via email."
                checked={subscribe}
                onChange={(e) => setSubscribe(e.target.checked)}
            />
            {errorMessage && 
            <Box mt={2} mb={2}>
            <Alert severity="error">{errorMessage}</Alert>
            </Box>
            }
            <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
            >
                SIGN UP
            </Button>
            <Typography align="center" sx={{ mt: 2 }}>
                  Already have an account? 
                  <Button onClick={() => navigate('/login')}>
                      Sign in
                  </Button>
            </Typography>
        </Box>
    )
};

export default RegisterForm;