// TableSelectDropdown.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx'; // Import API_URL

function TableSelectDropdown({ onTableSelect }) {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');

  const fetchTables = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}tables/`); // Using API_URL
      setTables(response.data);
      if (!response.data.includes(selectedTable)) {
        setSelectedTable('');
        onTableSelect(''); // Update the parent component's state
      }
    } catch (error) {
      console.error('Error fetching tables:', error);
    }
  }, [selectedTable, onTableSelect]); // Include selectedTable and onTableSelect as dependencies

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  const handleChange = (event) => {
    setSelectedTable(event.target.value);
    onTableSelect(event.target.value); // Update the parent component's state
  };

  return (
    <FormControl fullWidth>
      <InputLabel id="table-select-label">Select Table</InputLabel>
      <Select
        labelId="table-select-label"
        id="table-select"
        value={selectedTable}
        label="Select Table"
        onChange={handleChange}
      >
        {tables.map((table, index) => (
          <MenuItem key={index} value={table}>
            {table}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

export default TableSelectDropdown;
