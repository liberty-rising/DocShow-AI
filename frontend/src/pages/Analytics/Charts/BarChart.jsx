import React from 'react';
import { ResponsiveBar } from '@nivo/bar';

const mockData = [
  { product: "Product A", sales: 200, expenses: 150, profit: 50 },
  { product: "Product B", sales: 300, expenses: 200, profit: 100 },
  { product: "Product C", sales: 150, expenses: 100, profit: 50 },
  // ... add more data as needed
];

const BarChartComponent = ({ data }) => (
  <div style={{ height: "400px" }}>
    <ResponsiveBar data={mockData} keys={['sales']} indexBy="product" />
  </div>
);

export default BarChartComponent;
