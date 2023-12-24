import React, { useState } from 'react';
import { Alert, Box, Button, Grid, Paper, Snackbar, TextField, Typography } from '@mui/material';

const ChangePassword = ({ handleChangePassword, errorMessage, successMessage }) => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const success = await handleChangePassword(oldPassword, newPassword, confirmPassword);
    if (success) {
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    }
  };

  return (
    <Grid item xs={12}>
      <Paper elevation={3}>
        <Box p={3}>
          <Typography variant="h6">Change Password</Typography>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="oldPassword"
            label="Old Password"
            type="password"
            id="oldPassword"
            autoComplete="current-password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="newPassword"
            label="New Password"
            type="password"
            id="newPassword"
            autoComplete="current-password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="confirmPassword"
            label="Confirm New Password"
            type="password"
            id="confirmPassword"
            autoComplete="current-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {successMessage && 
            <Box mt={2} mb={2}>
              <Alert severity="success">{successMessage}</Alert>
            </Box>
          }
          {errorMessage && 
            <Box mt={2} mb={2}>
              <Alert severity="error">{errorMessage}</Alert>
            </Box>
          }
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleSubmit}
          >
            Change Password
          </Button>
        </Box>
      </Paper>
    </Grid>
  );
};

export default ChangePassword;