// OrganizationManagement.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx';
import { Button, Card, CardContent, TextField, Typography } from '@mui/material';

function OrganizationManagement() {
  const [organizationName, setOrganizationName] = useState('');

  const handleAddOrganization = () => {
    axios.post(`${API_URL}organizations/add`, { name: organizationName })
      .then(response => {
        // Handle successful addition
        console.log('Organization added:', response.data);
        setOrganizationName(''); // Reset the input field
      })
      .catch(error => {
        // Handle error
        console.error('Error adding organization', error);
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
    </Card>
  );
}

export default OrganizationManagement;
