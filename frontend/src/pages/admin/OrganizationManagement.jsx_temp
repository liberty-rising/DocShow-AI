// OrganizationManagement.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx';
import { Button, Card, CardContent, TextField, Typography, Snackbar, Alert, Select, MenuItem, Box } from '@mui/material';

function OrganizationManagement() {
  const [organizationName, setOrganizationName] = useState('');
  const [organizations, setOrganizations] = useState([]);
  const [selectedOrganization, setSelectedOrganization] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success'); // 'error' or 'success'

  useEffect(() => {
    // Fetch organizations when the component mounts
    fetchOrganizations();
  }, []);

  const fetchOrganizations = () => {
    axios.get(`${API_URL}organizations/`)
        .then(response => {
            setOrganizations(response.data);
        })
        .catch(error => {
            console.error('Error fetching organizations', error);
        });
  };

  const handleAddOrganization = () => {
    axios.post(`${API_URL}organization/`, { name: organizationName })
      .then(response => {
        setSnackbarMessage('Organization added successfully.');
        setSnackbarSeverity('success');
        setOpenSnackbar(true);
        setOrganizationName('');
        fetchOrganizations(); // Refresh the list of organizations
      })
      .catch(error => {
        setSnackbarMessage('Error adding organization.');
        setSnackbarSeverity('error');
        setOpenSnackbar(true);
      });
  };

  const handleDeleteOrganization = () => {
    axios.delete(`${API_URL}organization/${selectedOrganization}`)
      .then(response => {
        setSnackbarMessage('Organization deleted successfully.');
        setSnackbarSeverity('success');
        setOpenSnackbar(true);
        fetchOrganizations(); // Refresh the list of organizations
      })
      .catch(error => {
        setSnackbarMessage('Error deleting organization.');
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
        <Box mt={1}> {/* Added margin top */}
          <Button
            variant="contained"
            onClick={handleAddOrganization}
            disabled={!organizationName}
          >
            Add Organization
          </Button>
        </Box>

        <Box mt={2}> {/* Added margin top to the dropdown as well */}
          <Select
            value={selectedOrganization}
            onChange={e => setSelectedOrganization(e.target.value)}
            fullWidth
            displayEmpty
          >
            <MenuItem value="" disabled>Select Organization</MenuItem>
            {organizations.map(org => (
              <MenuItem key={org.id} value={org.id}>{org.name}</MenuItem>
            ))}
          </Select>
        </Box>
        <Box mt={2}>
        <Button
          variant="contained"
          color="error"
          onClick={handleDeleteOrganization}
          disabled={!selectedOrganization}
        >
          Delete Organization
        </Button>
        </Box>

      </CardContent>
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Card>
  );
}

export default OrganizationManagement;
