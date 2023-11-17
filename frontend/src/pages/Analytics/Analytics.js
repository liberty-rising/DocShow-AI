// AnalyticsPage.js
import React, { useState } from 'react';
import { Box, Typography } from '@mui/material';
import DashboardSelector from './DashboardSelector';
import ChartAdder from './ChartAdder';
import ChartDataSelector from './ChartDataSelector';
import ChartDisplay from './ChartDisplay';

function AnalyticsPage() {
  const [selectedDashboard, setSelectedDashboard] = useState('');
  const [chartType, setChartType] = useState('');
  const [selectedData, setSelectedData] = useState([]);

  // Mock data fetching
  const fetchData = (columns) => {
    // Fetch data based on selected columns
  };

  const handleDashboardSelect = (dashboard) => {
    setSelectedDashboard(dashboard);
    // Load dashboard data or set up a new dashboard
  };

  const handleAddChart = (type) => {
    setChartType(type);
    // Reset data selection
    setSelectedData([]);
  };

  const handleDataSelect = (e) => {
    // Add or remove data based on selection
    const column = e.target.value;
    if (e.target.checked) {
      setSelectedData([...selectedData, column]);
    } else {
      setSelectedData(selectedData.filter(item => item !== column));
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>📊 Data Analytics</Typography>
      <DashboardSelector onSelectDashboard={handleDashboardSelect} />
      <ChartAdder onAddChart={handleAddChart} />
      {chartType && <ChartDataSelector chartType={chartType} onDataSelect={handleDataSelect} />}
      <ChartDisplay chartType={chartType} data={fetchData(selectedData)} />
    </Box>
  );
}

export default AnalyticsPage;
