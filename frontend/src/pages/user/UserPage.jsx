import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EmailIcon from '@mui/icons-material/Email';
import BusinessIcon from '@mui/icons-material/Business';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { Alert, Box, CircularProgress, Grid, Snackbar, Typography } from '@mui/material';
import InfoCard from './InfoCard';
import ChangePassword from './ChangePassword';
import { API_URL } from '../../utils/constants';

const UserPage = () => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [organizationData, setOrganizationData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    setIsLoading(true);
    const fetchData = async () => {
      try {
        const userResponse = await axios.get(`${API_URL}users/me/`);
        const userData = userResponse.data;
        setUserData(userData);

        // Fetch organization data if organization_id is present
        if (userData.organization_id) {
          const orgResponse = await axios.get(`${API_URL}organization/`, { 
            params: { org_id: userData.organization_id } 
          });
          setOrganizationData(orgResponse.data);
        }
      } catch (error) {
        setError(error.response ? error.response.data.message : error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChangePassword = async (oldPassword, newPassword, confirmPassword) => {
    if (newPassword !== confirmPassword) {
      setErrorMessage('Passwords do not match!');
      return;
    }
  
    try {
      const response = await axios.put(`${API_URL}users/change-password/`, { old_password: oldPassword, new_password: newPassword });
  
      if (response.status === 200) {
        setSuccessMessage('Password changed successfully');
        setErrorMessage('');
        return true;  
      } else {
        setErrorMessage('Failed to change password!');
        return false;
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
      return false;
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, marginBottom: 2 }}>
        <Typography variant="h4" gutterBottom>👤 User Panel</Typography>
      </Box>

      {isLoading ? (
        <CircularProgress />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : userData ? (
        <Grid container spacing={2}>
          <InfoCard Icon={AccountCircleIcon} title="Username" content={userData.username} />
          <InfoCard Icon={EmailIcon} title="Email" content={userData.email} />
          <InfoCard Icon={BusinessIcon} title="Organization" content={organizationData ? organizationData.name : 'N/A'} />
          <InfoCard Icon={AssignmentIndIcon} title="Role" content={userData.role} />
        </Grid>
      ) : (
        <Typography variant="body1">User details not available.</Typography>
      )}
      <Box sx={{ height: 16 }} />
      <ChangePassword handleChangePassword={handleChangePassword} errorMessage={errorMessage} successMessage={successMessage}/>
    </Box>
  );
};

export default UserPage;
