import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Select, MenuItem, FormControl, InputLabel, Button } from '@mui/material';

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState('');

  useEffect(() => {
    axios.get('https://127.0.0.1/data-profiling') // Replace with your actual backend URL
      .then(response => {
        setDataProfiles(response.data);
      })
      .catch(error => console.error('Error fetching data profiles:', error));
  }, []);

  const handleChange = (event) => {
    setSelectedProfile(event.target.value);
  };

  const handleExtractData = () => {
    axios.post('https://127.0.0.1/data-profiling', { profileId: selectedProfile }) // Replace with your actual backend URL
      .then(response => {
        // Handle the response
        console.log('Data extracted:', response.data);
      })
      .catch(error => {
        console.error('Error extracting data:', error);
      });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>🔍 Data Profiling</Typography>
      <FormControl fullWidth>
        <InputLabel id="data-profile-select-label">Select all the elements to extract</InputLabel>
        <Select
          labelId="data-profile-select-label"
          id="data-profile-select"
          value={selectedProfile}
          label="Data Profile"
          onChange={handleChange}
        >
          {dataProfiles.map(profile => (
            <MenuItem key={profile.id} value={profile.id}>
              {profile.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button
        variant="contained"
        color="primary"
        onClick={handleExtractData}
        sx={{ mt: 2 }}
      >
        Extract Data
      </Button>
      {/* Other content */}
    </Box>
  );
}

export default DataProfilingPage;
