import React from 'react';
import { Box, Typography } from '@mui/material';
import { ResponsiveBar } from '@nivo/bar';

const mockData = [
  {sales: 3919615.659999997, productline: 'Classic Cars'},
  {sales: 226243.46999999997, productline: 'Trains'},
  {sales: 975003.5700000001, productline: 'Planes'},
  {sales: 1127789.8399999996, productline: 'Trucks and Buses'},
  {sales: 1903150.8399999992, productline: 'Vintage Cars'},
  {sales: 1166388.3400000003, productline: 'Motorcycles'},
  {sales: 714437.13, productline: 'Ships'}
];

const BarChartComponent = ({ config }) => (
  <Box>
    <Typography variant="subtitle1" gutterBottom>{config.title}</Typography>
    <div style={{ height: "400px" }}>
      <ResponsiveBar data={config.data} keys={config.keys} indexBy={config.index_by} />
      {/* <ResponsiveBar data={config.data} keys={config.keys} indexBy={config.index_by} /> */}
    </div>
  </Box>
);

export default BarChartComponent;
