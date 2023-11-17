import React, { useState } from 'react';
import axios from 'axios';
import qs from 'qs';
import { Box, Button, Container, TextField, Typography } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../utils/constants';

function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { updateAuth } = useAuth();

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
        const response = await axios.post(`${API_URL}token/`, qs.stringify ({
            username,
            password
        }), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        // Assuming the backend sets the cookie automatically
        // If login is successful, navigate to root
        if (response.status === 200) {
            // Here you might want to do additional checks or set state
            updateAuth(true);
            navigate('/'); 
        }
    } catch (error) {
        console.error('Login error:', error);
        // Handle login error (e.g., show an error message)
    }
  };

  const handleRegister = () => {
    navigate('/register');
  };

  return (
    <Container component="main" maxWidth="xs">
        <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            <Typography component="h1" variant="h5">
                Login
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
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
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Sign In
                </Button>
                <Button
                    type="button"
                    fullWidth
                    variant="outlined"
                    onClick={handleRegister}
                    sx={{ mt: 1, mb: 2 }}
                >
                    Register
                </Button>
            </Box>
        </Box>
    </Container>
  );
}

export default LoginPage;
