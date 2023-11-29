import React from 'react';
import BarChartComponent from './Components/BarChart';
import LineChartComponent from './Components/LineChart';
import PieChartComponent from './Components/PieChart';

const ChartDisplay = ({ chartType, config }) => {
  switch(chartType) {
    case 'bar':
      return <BarChartComponent chartConfig={config} />;
    case 'line':
      return <LineChartComponent config={config} />;
    case 'pie':
      return <PieChartComponent config={config} />;
    default:
      return <p>Select a chart type</p>;
  }
};

export default ChartDisplay;
