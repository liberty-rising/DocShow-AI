import React from 'react';
import BarChartComponent from './Charts/BarChart';
import LineChartComponent from './Charts/LineChart';
import PieChartComponent from './Charts/PieChart';

const ChartDisplay = ({ chartType, config }) => {
  switch(chartType) {
    case 'bar':
      return <BarChartComponent config={config} />;
    case 'line':
      return <LineChartComponent config={config} />;
    case 'pie':
      return <PieChartComponent config={config} />;
    default:
      return <p>Select a chart type</p>;
  }
};

export default ChartDisplay;
