import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Box, Container, Typography } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import RegisterForm from './RegisterForm';
import { useAuth } from '../../contexts/AuthContext';
import { API_URL } from '../../utils/constants';

function RegisterPage() {
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const { updateAuth } = useAuth();

  const handleSubmit = async (username, email, password, subscribe, marketingContent) => {
    try {
        const response = await axios.post(`${API_URL}register/`, {
            username,
            email,
            password,
            subscribe,
            marketingContent,
        });

        if (response.data.message === 'Registration successful') {
            updateAuth(true);
            // Call the send-verification-email endpoint
            await axios.post(`${API_URL}users/send-verification-email/`, {
              email,
            });

            // Navigate to the verify-email page instead of login
            navigate('/verify-email', { state: { email } });
        }
    } catch (error) {
        if (error.response) {
            if (error.response.status === 400) {
              setErrorMessage(error.response.data.detail);
            } else if (error.response.data && error.response.data.detail && error.response.data.detail[0]) {
              let errorMessage = error.response.data.detail[0].msg;
              if (typeof errorMessage === 'string') {
                errorMessage = errorMessage.replace('Value error, ', '');
                setErrorMessage(errorMessage);
              }
            }
          } else if (error.request) {
            // The request was made but no response was received
            console.log(error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message)
          }
        }
    }

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
          <RegisterForm onSubmit={handleSubmit} errorMessage={errorMessage} />
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 5 }}>
              Copyright © DocShow AI 2024.
          </Typography>
      </Box>
    </Container>
  );
};

export default RegisterPage;
