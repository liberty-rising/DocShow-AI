// AnalyticsPage.js
import React, { useEffect, useState } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import AIAssistant from './AIAssistant';
import TableSelectDropdown from '../../components/tables/selects/TableSelectDropdown';
import { fetchOrganizationTables } from '../../api/organizationTables';

function AnalyticsPage() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [tableData, setTableData] = useState(null);

  useEffect(() => {
    const getOrganizationTables = async () => {
      const data = await fetchOrganizationTables();
      setTables(data);
    };

    getOrganizationTables();
  }, []);

  const handleTableSelect = async (table) => {
    setSelectedTable(table);
    const data = await fetchOrganizationTables(table); // fetchTableData is your API call function
    setTableData(data);
  };

  useEffect(() => {
    if (selectedTable) {
      handleTableSelect(selectedTable);
    }
  }, [selectedTable]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>📊 Data Analytics</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TableSelectDropdown tables={tables} selectedTable={selectedTable} onTableSelect={handleTableSelect} />
        </Grid>
        <Grid item xs={12}>
          <AIAssistant />
        </Grid>
      </Grid>
    </Box>
  );
}

export default AnalyticsPage;