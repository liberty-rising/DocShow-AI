import React from 'react';
import { Box, Typography } from '@mui/material';
import { ResponsiveLine } from '@nivo/line';

const LineChartComponent = ({ config }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{config.title}</Typography>
    <div style={{ height: "400px" }}>
      <ResponsiveLine data={config.data} />
    </div>
  </Box>
);

export default LineChartComponent;
