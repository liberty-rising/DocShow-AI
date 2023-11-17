import React, { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import EmailIcon from '@mui/icons-material/Email';
import BusinessIcon from '@mui/icons-material/Business';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { API_URL } from '../utils/constants';

const UserPage = () => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}users/me/`);
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        } else {
          throw new Error('Failed to fetch user details.');
        }
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

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
          {/* Username Card */}
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <AccountCircleIcon />
                <Typography variant="h6">Username</Typography>
                <Typography variant="body1">{userData.username}</Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Email Card */}
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <EmailIcon />
                <Typography variant="h6">Email</Typography>
                <Typography variant="body1">{userData.email}</Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Organization Card */}
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <BusinessIcon />
                <Typography variant="h6">Organization</Typography>
                <Typography variant="body1">{userData.organization}</Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Role Card */}
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <AssignmentIndIcon />
                <Typography variant="h6">Role</Typography>
                <Typography variant="body1">{userData.role}</Typography>
              </CardContent>
            </Card>
          </Grid>
          {/* Additional Cards or Components */}
        </Grid>
      ) : (
        <Typography variant="body1">User details not available.</Typography>
      )}
    </Box>
  );
};

export default UserPage;
