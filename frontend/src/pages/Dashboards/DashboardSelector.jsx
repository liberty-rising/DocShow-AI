import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const DashboardSelector = ({ selectedDashboard, onSelectDashboard }) => {
  const [dashboards, setDashboards] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/dashboards/`)
      .then(response => {
        const dashboardNames = response.data.map(dashboard => dashboard.name);
        setDashboards(dashboardNames);
      })
      .catch(error => {
        console.error('Error fetching dashboards', error);
      });
  }, []);

  return (
    <FormControl fullWidth>
      <InputLabel id="dashboard-select-label">Select Dashboard</InputLabel>
      <Select
        labelId="dashboard-select-label"
        value={selectedDashboard}
        label="Select Dashboard"
        onChange={(e) => onSelectDashboard(e.target.value)}
      >
        {dashboards.map(dashboard => (
          <MenuItem key={dashboard} value={dashboard}>
            {dashboard}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default DashboardSelector;
