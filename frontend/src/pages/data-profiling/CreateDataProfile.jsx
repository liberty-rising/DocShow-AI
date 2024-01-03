import React, { useState } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../../utils/constants';

const CreateDataProfile = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post(`${API_URL}data-profile/`, { name, description })
      .then(response => {
        // Handle successful data profile creation
        console.log('Data Profile created:', response.data);
        navigate('/data-profiling')
      })
      .catch(error => {
        console.error('Error creating data profile:', error);
      });
  };

  const handleBack = () => {
    navigate('/data-profiling')
  }

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
      <Typography variant="h6">Create New Data Profile</Typography>
      <TextField
        required
        fullWidth
        label="Name"
        value={name}
        onChange={e => setName(e.target.value)}
        margin="normal"
      />
      <TextField
        required
        fullWidth
        label="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
        margin="normal"
      />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        Create Data Profile
      </Button>
      <Button fullWidth variant="outlined" sx={{ mt: 1 }} onClick={handleBack}>
        Back to Data Profiling
      </Button>
    </Box>
  );
};

export default CreateDataProfile;
