import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from '@mui/material';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { API_URL } from '../../utils/constants';

function DashboardTable() {
  const [dashboards, setDashboards] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/dashboards/`)
      .then(response => response.json())
      .then(data => setDashboards(data))
      .catch(error => console.error('Error fetching dashboards:', error));
  }, []);

  return (
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
            <TableCell style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                <Tooltip title={dashboard.description} placement="top">
                    <div>{dashboard.description}</div>
                </Tooltip>
            </TableCell>
            <TableCell>{format(new Date(dashboard.created_at), 'yyyy-MM-dd')}</TableCell>
            <TableCell>{format(new Date(dashboard.updated_at), 'yyyy-MM-dd')}</TableCell>
        </TableRow>
        ))}
    </TableBody>
    </Table>
  );
}

export default DashboardTable;
