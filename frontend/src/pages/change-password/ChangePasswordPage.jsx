import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { Box, Container } from '@mui/material'
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import ChangePassword from '../../components/change-password/ChangePassword';
import { updateUserPassword } from '../../utils/updateUserPassword';

function ChangePasswordPage() {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleChangePassword = async (oldPassword, newPassword, confirmPassword) => {
        const success = await updateUserPassword(oldPassword, newPassword, confirmPassword, setErrorMessage, setSuccessMessage);
        if (success) {
            navigate('/dashboards');
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
                {/* <Typography component="h1" variant="h5">
                    Change Password
                </Typography> */}
                <ChangePassword handleChangePassword={handleChangePassword} errorMessage={errorMessage} successMessage={successMessage} />
            </Box>
        </Container>
    )
}

export default ChangePasswordPage