import React from 'react';
import { ResponsiveBar } from '@nivo/bar';

const BarChartComponent = ({ data }) => (
  <div style={{ height: "400px" }}>
    <ResponsiveBar
      data={data}
      keys={['sales']}
      indexBy="product"
      margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
      padding={0.3}
      valueScale={{ type: 'linear' }}
      indexScale={{ type: 'band', round: true }}
      colors={{ scheme: 'set3' }}
    />
  </div>
);

export default BarChartComponent;
