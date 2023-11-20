import React from 'react';

const ChartAdder = ({ onAddChart }) => {
  const chartTypes = ['Bar', 'Line', 'Pie'];

  return (
    <select onChange={(e) => onAddChart(e.target.value)}>
      <option value="">Add Chart</option>
      {chartTypes.map(type => (
        <option key={type} value={type}>{type} Chart</option>
      ))}
    </select>
  );
};

export default ChartAdder;
