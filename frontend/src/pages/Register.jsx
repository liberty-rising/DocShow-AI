import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Checkbox, Container, FormControlLabel, TextField, Typography } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { API_URL } from '../utils/constants';

function RegisterPage({ onRegister }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [subscribe, setSubscribe] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
        const response = await axios.post(`${API_URL}register/`, {
            username,
            email,
            password,
            // You can add subscribe or any additional fields if required by your API
        });

        if (response.status === 200) {
            navigate('/login');
        }
    } catch (error) {
        console.error('Registration error:', error);
        // Handle registration error (e.g., show an error message)
    }
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
          <LockOutlinedIcon color="secondary" sx={{ m: 1, bgcolor: 'background.paper', borderRadius: '50%' }} />
          <Typography component="h1" variant="h5">
              Sign up
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
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 5 }}>
              Copyright © Your Website 2023.
          </Typography>
      </Box>
    </Container>
);
}

export default RegisterPage;
