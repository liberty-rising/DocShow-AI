import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Select, MenuItem, FormControl, InputLabel, Button } from '@mui/material';
import { API_URL } from '../../utils/constants';

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState('');

  useEffect(() => {
    axios.get(`${API_URL}data-profiles/`)
      .then(response => {
        // Check if the response is an array before updating state
        if (Array.isArray(response.data)) {
          setDataProfiles(response.data);
        } else {
          console.error('Received data is not an array:', response.data);
          // Optionally set an empty array or handle this scenario appropriately
          setDataProfiles([]);
        }
      })
      .catch(error => {
        console.error('Error fetching data profiles:', error);
        setDataProfiles([]); // Reset to empty array on error
      });
  }, []);

  const handleChange = (event) => {
    setSelectedProfile(event.target.value);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>🔍 Data Profiling</Typography>
      <FormControl fullWidth>
        <InputLabel id="data-profile-select-label">Data Profile</InputLabel>
        <Select
          labelId="data-profile-select-label"
          id="data-profile-select"
          value={selectedProfile}
          label="Data Profile"
          onChange={handleChange}
        >
          {dataProfiles.map((profile, index) => (
            <MenuItem key={index} value={profile.id}>
              {profile.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}

export default DataProfilingPage;
