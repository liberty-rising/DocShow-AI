// AnalyticsPage.js
import React, { useState } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import AIAssistant from './AIAssistant';
import TableSelectDropdown from './TableSelectDropdown';
// import other components as needed

function AnalyticsPage() {
  const [chartType, setChartType] = useState('');
  const [selectedData, setSelectedData] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');

  // Mock data fetching
  const fetchData = (columns) => {
    const mockData = [
      { product: "Product A", sales: 200, expenses: 150, profit: 50 },
      { product: "Product B", sales: 300, expenses: 200, profit: 100 },
      { product: "Product C", sales: 150, expenses: 100, profit: 50 },
      // ... add more data as needed
    ];

    if (!columns || columns.length === 0) {
      return [];
    }

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
    setSelectedData([]);
  };

  const handleDataSelect = (e) => {
    const column = e.target.value;
    if (e.target.checked) {
      setSelectedData([...selectedData, column]);
    } else {
      setSelectedData(selectedData.filter(item => item !== column));
    }
  };

  const handleTableSelect = (table) => {
    setSelectedTable(table);
    // You can also fetch table data here if needed
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>📊 Data Analytics</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TableSelectDropdown onTableSelect={handleTableSelect} />
        </Grid>
        <Grid item xs={12}>
          {/* AI Assistant */}
          <AIAssistant />
        </Grid>
        {/* Other components */}
      </Grid>
    </Box>
  );
}

export default AnalyticsPage;