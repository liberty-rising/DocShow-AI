import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Grid, IconButton, Paper, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline'
import { useNavigate } from 'react-router-dom';
import ChartDisplay from './Charts/ChartDisplay';
import { API_URL } from '../../utils/constants';

function Dashboard() {
  const { dashboardId } = useParams();
  const [dashboardData, setDashboardData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (dashboardId) {
      fetch(`${API_URL}/dashboard/?id=${dashboardId}`)
        .then(response => response.json())
        .then(data => setDashboardData(data))
        .catch(error => console.error('Error fetching dashboard:', error));
    }
  }, [dashboardId]);

  const handleChartCreate = (event) => {
    navigate(`/dashboards/${dashboardId}/charts/create`)
  }

  if (!dashboardData) return <div>Loading...</div>;
  console.log(dashboardData.charts[2].config)
  return (
    <div>
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>📊 {dashboardData.name} </Typography>
        <Typography variant="subtitle1" gutterBottom>Description: {dashboardData.description}</Typography>
        <Grid container spacing={2}>
          {dashboardData.charts && dashboardData.charts.map((chart, index) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
              <Paper elevation={3} sx={{ padding: 2 }}>
                <ChartDisplay chartType={chart.config.type} config={chart.config} />
              </Paper>
            </Grid>
          ))}
          <Grid item xs={12} sm={6} md={4} lg={3}>
            <Paper elevation={3} sx={{ padding: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <IconButton color="primary" aria-label="add new chart" onClick={handleChartCreate}>
                <AddCircleOutlineIcon style={{ fontSize: 60 }} />
              </IconButton>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}

export default Dashboard;
