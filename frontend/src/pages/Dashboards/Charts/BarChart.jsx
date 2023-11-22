import React from 'react';
import { Box, Typography } from '@mui/material';
import { ResponsiveBar } from '@nivo/bar';

const BarChartComponent = ({ config }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{config.title}</Typography>
    <div style={{ height: "400px" }}>
      <ResponsiveBar data={config.data} keys={config.keys} indexBy={config.indexBy} />
      {/* <ResponsiveBar data={config.data} keys={config.keys} indexBy={config.index_by} /> */}
    </div>
  </Box>
);

export default BarChartComponent;
