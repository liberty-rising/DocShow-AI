import React from 'react';
import { Box, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import DashboardTable from './DashboardTable';

function DashboardMenuPage() {

  const handleCreateDashboard = () => {
    // Logic to create a new dashboard
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>📊 Dashboards</Typography>
      <Button variant="contained" onClick={handleCreateDashboard} sx={{ mb: 2 }}>
        Create New Dashboard
      </Button>
      <DashboardTable />
    </Box>
  );
}

export default DashboardMenuPage;
