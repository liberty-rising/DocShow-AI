// TableManagement.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants';
import { Card, CardContent, Typography, Select, MenuItem, Button, Grid, FormControl, InputLabel } from '@mui/material';

function TableManagement() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = () => {
    axios.get(`${API_URL}tables/`)
      .then(response => {
        setTables(response.data);
        if (!response.data.includes(selectedTable)) {
          setSelectedTable('');
        }
      })
      .catch(error => console.error('Error fetching tables', error));
  };

  const handleDropTable = () => {
    axios.delete(`${API_URL}table/`, { params: { table_name: selectedTable } })
      .then(response => {
        fetchTables(); // Refresh the tables list
      })
      .catch(error => {
        console.error('Error dropping table', error);
      });
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Table Management</Typography>
        <Grid container spacing={2} alignItems="center" sx={{ marginTop: 2 }}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel id="select-table-label">Select Table</InputLabel>
              <Select
                labelId="select-table-label"
                value={selectedTable}
                onChange={e => setSelectedTable(e.target.value)}
                label="Select Table"
              >
                {tables.map(table => <MenuItem key={table} value={table}>{table}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Button variant="contained" onClick={handleDropTable} fullWidth>Drop Table</Button>
          </Grid>
          {/* <Grid item xs={12} sm={3}>
            <Button variant="contained" onClick={fetchTables} fullWidth>Refresh</Button>
          </Grid> */}
        </Grid>
      </CardContent>
    </Card>
  );
}

export default TableManagement;
