// AnalyticsPage.js
import React, { useState } from 'react';
import { Box, Typography } from '@mui/material';
// import ChartAdder from './ChartAdder';
// import ChartDataSelector from './ChartDataSelector';
// import ChartDisplay from './ChartDisplay';

function AnalyticsPage() {
  const [chartType, setChartType] = useState('');
  const [selectedData, setSelectedData] = useState([]);

  // Mock data fetching
  const fetchData = (columns) => {
    // Mock dataset
    const mockData = [
      { product: "Product A", sales: 200, expenses: 150, profit: 50 },
      { product: "Product B", sales: 300, expenses: 200, profit: 100 },
      { product: "Product C", sales: 150, expenses: 100, profit: 50 },
      // ... add more data as needed
    ];

    // If no columns are selected, return an empty array
    if (!columns || columns.length === 0) {
      return [];
    }

    // Filter the data based on selected columns
    return mockData.map(row => {
      const filteredRow = { product: row.product };
      columns.forEach(column => {
        filteredRow[column] = row[column];
      });
      return filteredRow;
    });
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
    <Box>
      <Typography variant="h4" gutterBottom>📊 Data Analytics</Typography>
      {/* <ChartAdder onAddChart={handleAddChart} />
      {chartType && <ChartDataSelector chartType={chartType} onDataSelect={handleDataSelect} />} */}
    </Box>
  );
}

export default AnalyticsPage;
