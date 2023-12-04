import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState('');

  useEffect(() => {
    axios.get('https://127.0.0.1/data-profiling')
      .then(response => {
        setDataProfiles(response.data);
      })
      .catch(error => console.error('Error fetching data profiles:', error));
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
          {dataProfiles.map(profile => (
            <MenuItem key={profile.id} value={profile.id}>
              {profile.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {/* Other content */}
    </Box>
  );
}

export default DataProfilingPage;