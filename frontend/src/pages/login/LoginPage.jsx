import React, { useEffect, useState } from 'react';
import axios from 'axios';
import qs from 'qs';
import { Box, Button, Checkbox, Container, FormControlLabel, TextField, Typography } from '@mui/material';
import Alert from '@mui/material/Alert';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import validator from 'validator';
import { API_URL } from '../../utils/constants';

function LoginPage({ onLogin }) {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();
  const { updateAuth, updateEmailVerification } = useAuth();
  const [errorMessage, setErrorMessage] = useState(''); 

 
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Determine if usernameOrEmail should be sent as username or email
    const isEmail = validator.isEmail(usernameOrEmail);
    const data = isEmail 
        ? { email: usernameOrEmail, password, remember: rememberMe } 
        : { username: usernameOrEmail, password, remember: rememberMe };

    try {
        const response = await axios.post(`${API_URL}token/`, qs.stringify (data), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        if (response.status === 200) {
            updateAuth(true);
            const userResponse = await axios.get(`${API_URL}users/me/`, {
                headers: {
                    'Authorization': `Bearer ${response.data.access_token}`
                }
            });
            if (userResponse.data.requires_password_update) {
                navigate('/change-password'); 
            } else if (userResponse.data.email_verified == false) {
                console.log("email_verified is false")
                navigate('/verify-email');
            } else {
                console.log("email_verified is true")
                updateEmailVerification(true);
                navigate('/dashboards')
            } 
        }
    } catch (error) {
        if (error.response && error.response.status === 401) {
            // Handle 401 error here
            setErrorMessage('Invalid credentials');
        } else {
            setErrorMessage(`Login error: ${error.message}`);
        }
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
          <LockOutlinedIcon color="secondary" sx={{ m: 1, bgcolor: 'background.paper', borderRadius: '50%' }} />
          <Typography component="h1" variant="h5">
              Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
              <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Username or Email"
                  name="usernameOrEmail"
                  autoComplete="username"
                  autoFocus
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
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
              <FormControlLabel
                  control={<Checkbox value="remember" color="primary" />}
                  label="Remember me"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
              />
              {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
              <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
              >
                  Sign In
              </Button>
              <Typography align="center" sx={{ mt: 2 }}>
                  <Button onClick={() => navigate('/forgot-password')}>
                      Forgot password?
                  </Button>
                  <Button onClick={handleRegister}>
                      Don't have an account? Sign Up
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

export default LoginPage;
