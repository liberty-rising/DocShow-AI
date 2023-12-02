// OrganizationManagement.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx';
import { Button, Card, CardContent, TextField, Typography, Snackbar, Alert } from '@mui/material';

function OrganizationManagement() {
  const [organizationName, setOrganizationName] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success'); // 'error' or 'success'

  const handleAddOrganization = () => {
    axios.post(`${API_URL}organizations/add`, { name: organizationName })
      .then(response => {
        // Handle successful addition
        console.log('Organization added:', response.data);
        setSnackbarMessage('Organization added successfully.');
        setSnackbarSeverity('success');
        setOpenSnackbar(true);
        setOrganizationName(''); // Reset the input field
      })
      .catch(error => {
        // Handle error
        console.error('Error adding organization', error);
        setSnackbarMessage('Error adding organization.');
        setSnackbarSeverity('error');
        setOpenSnackbar(true);
      });
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Organization Management</Typography>
        <TextField
          label="Organization Name"
          value={organizationName}
          onChange={e => setOrganizationName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <Button 
          variant="contained" 
          onClick={handleAddOrganization} 
          disabled={!organizationName}
        >
          Add Organization
        </Button>
      </CardContent>

      {/* Snackbar for showing notifications */}
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Card>
  );
}

export default OrganizationManagement;
