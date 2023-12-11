import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Link, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../../utils/constants';

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_URL}data-profiles/`)
      .then(response => {
        if (Array.isArray(response.data)) {
          setDataProfiles(response.data);
        } else {
          console.error('Received data is not an array:', response.data);
          setDataProfiles([]);
        }
      })
      .catch(error => console.error('Error fetching data profiles:', error));
  }, []);

  const handleProfileClick = (dataProfileId) => {
    navigate(`/data-profiling/${dataProfileId}`);
  };

  const handleCreateNewProfile = () => {
    navigate('/data-profiling/create');
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>🔍 Data Profiling</Typography>
      <Button 
        variant="contained" 
        color="primary" 
        onClick={handleCreateNewProfile} 
        sx={{ mb: 2 }}
      >
        Create New Data Profile
      </Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dataProfiles.map((profile) => (
              <TableRow key={profile.id}>
                <TableCell>
                  <Link component="button" variant="body2" onClick={() => handleProfileClick(profile.id)}>
                    {profile.name}
                  </Link>
                </TableCell>
                <TableCell>{profile.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default DataProfilingPage;
