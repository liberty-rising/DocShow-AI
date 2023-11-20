import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, FormControl, Grid, InputLabel, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material';
import axios from 'axios';
import { API_URL } from '../../utils/constants.jsx';

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedUser, setSelectedUser] = useState({});

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_URL}users/`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users', error);
    }
  };

  const fetchRoles = async () => {
    try {
      const response = await axios.get(`${API_URL}users/roles/`);
      setRoles(response.data);
    } catch (error) {
      console.error('Error fetching roles', error);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchRoles();
  }, []); // Empty dependency array since these functions don't depend on external variables

  const handleUpdateUser = async () => {
    const data = {
      username: selectedUser.username,
      organization: selectedUser.organization,
      role: selectedUser.role
    };

    try {
      await axios.put(`${API_URL}users/update/`, data);
      // Refetch users after update
      const response = await axios.get(`${API_URL}users/`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error updating user', error);
    }
  };

  const handleSelectUser = username => {
    const user = users.find(u => u.username === username);
    setSelectedUser(user || {});
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">User Management</Typography>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Username</TableCell>
                <TableCell>Organization</TableCell>
                <TableCell>Role</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.username}>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.organization}</TableCell>
                  <TableCell>{user.role}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Grid container spacing={2} alignItems="center" sx={{ marginTop: 2 }}>
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel id="select-user-label">Select User</InputLabel>
              <Select
                labelId="select-user-label"
                value={selectedUser.username || ''}
                onChange={e => handleSelectUser(e.target.value)}
                label="Select User"
              >
                {users.map(user => <MenuItem key={user.username} value={user.username}>{user.username}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField
              label="Organization"
              value={selectedUser.organization || ''}
              onChange={e => setSelectedUser({ ...selectedUser, organization: e.target.value })}
              fullWidth
              disabled={!selectedUser.username}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth disabled={!selectedUser.username}>
              <InputLabel id="select-role-label">Select Role</InputLabel>
              <Select
                labelId="select-role-label"
                value={selectedUser.role || ''}
                onChange={e => setSelectedUser({ ...selectedUser, role: e.target.value })}
                label="Select Role"
              >
                {roles.map(role => <MenuItem key={role} value={role}>{role}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button variant="contained" onClick={handleUpdateUser} disabled={!selectedUser.username}>Update</Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

export default UserManagement;