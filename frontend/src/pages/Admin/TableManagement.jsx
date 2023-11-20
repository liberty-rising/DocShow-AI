// TableManagement.js
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx';
import { Alert, Button, Card, CardContent, Dialog, DialogActions, DialogContent, DialogContentText,
  DialogTitle, FormControl, Grid, InputLabel, MenuItem, Select, Snackbar, Typography } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

function TableManagement() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [snackbarSeverity, setSnackbarSeverity] = useState('success'); // 'error' or 'success'


  const fetchTables = useCallback(() => {
    axios.get(`${API_URL}tables/`)
      .then(response => {
        setTables(response.data);
        if (!response.data.includes(selectedTable)) {
          setSelectedTable('');
        }
      })
      .catch(error => console.error('Error fetching tables', error));
  }, [selectedTable]); // Include selectedTable as dependency if it's used in the fetchTables function

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  const handleDropTable = () => {
    axios.delete(`${API_URL}table/`, { params: { table_name: selectedTable } })
      .then(response => {
        fetchTables(); // Refresh the tables list
        setSnackbarMessage('Table dropped successfully.');
        setSnackbarSeverity('success');
        setOpenSnackbar(true);
      })
      .catch(error => {
        console.error('Error dropping table', error);
        // Show error in snackbar
        setSnackbarMessage('Error dropping table.');
        setSnackbarSeverity('error');
        setOpenSnackbar(true);
      })
      .finally(() => {
        setOpenDialog(false); // Close the dialog
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

      {/* Snackbar for showing notifications */}
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>

      {/* Dialog for confirmation */}
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Confirm Table Deletion"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete this table? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button 
            variant="contained"
            color="error"
            onClick={() => setOpenDialog(true)}
            fullWidth
            startIcon={<DeleteIcon />}
            disabled={!selectedTable}
          >
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
}

export default TableManagement;
