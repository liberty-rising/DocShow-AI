import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';
import { API_URL } from '../../utils/constants';
import axios from 'axios';

const VerifyEmailPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const email = location.state?.email || null;

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const token = params.get('token');

        if (token) {
        axios.put(`${API_URL}users/verify-email/`, { token })
            .then(response => {
                // Handle successful verification
                navigate('/login');
            })
            .catch(error => {
            // Handle failed verification
            });
        }
    }, [location, navigate]);

    const handleResendEmail = async (event) => {
        event.preventDefault();
        axios.post(`${API_URL}users/send-verification-email/`, { email })
            .then(response => {
                // Handle successful email resend
                console.log('Verification email sent successfully');
            })
            .catch(error => {
                // Handle failed email resend
                console.log('Failed to send verification email');
            });
    };

    return (
        <Container maxWidth="sm">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Typography variant="h4" align="center" gutterBottom>
                    Verify Your Email
                </Typography>
                <Typography variant="body1" align="center" gutterBottom>
                    We've sent a verification link to your email address. Please check your inbox and click the link to verify your email.
                </Typography>
                <Button variant="contained" color="primary" fullWidth onClick={handleResendEmail}>
                    Resend Verification Email
                </Button>
            </Box>
        </Container>
    );
};

export default VerifyEmailPage;