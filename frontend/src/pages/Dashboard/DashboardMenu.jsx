import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { API_URL } from '../../utils/constants';

function DashboardMenuPage() {
  const [dashboards, setDashboards] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/dashboards/`)
      .then(response => response.json())
      .then(data => setDashboards(data))
      .catch(error => console.error('Error fetching dashboards:', error));
  }, []);

  const handleCreateDashboard = () => {
    // Logic to create a new dashboard
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>📊 Dashboards</Typography>
      <Button variant="contained" onClick={handleCreateDashboard} sx={{ mb: 2 }}>
        Create New Dashboard
      </Button>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Created at</TableCell>
            <TableCell>Updated at</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {dashboards.map((dashboard) => (
            <TableRow key={dashboard.name} hover>
              <TableCell>
                <Link to={`/dashboards/${dashboard.id}`}>{dashboard.name}</Link>
              </TableCell>
              <TableCell>{dashboard.description}</TableCell>
              <TableCell>{format(new Date(dashboard.created_at), 'yyyy-MM-dd')}</TableCell>
              <TableCell>{format(new Date(dashboard.updated_at), 'yyyy-MM-dd')}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
}

export default DashboardMenuPage;
