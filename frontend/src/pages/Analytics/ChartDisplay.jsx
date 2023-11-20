import React from 'react';
import BarChartComponent from './Charts/BarChart';
import LineChartComponent from './Charts/LineChart';
import PieChartComponent from './Charts/PieChart';

const ChartDisplay = ({ chartType, data }) => {
  const mockChartType = 'Bar'
  switch(mockChartType) {
    case 'Bar':
      return <BarChartComponent data={data} />;
    case 'Line':
      return <LineChartComponent data={data} />;
    case 'Pie':
      return <PieChartComponent data={data} />;
    default:
      return <p>Select a chart type</p>;
  }
};

export default ChartDisplay;
