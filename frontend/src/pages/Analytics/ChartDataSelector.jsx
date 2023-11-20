// ChartDataSelector.js
import React from 'react';

const ChartDataSelector = ({ chartType, onDataSelect }) => {
  // Mock columns, ideally load from your data source
  const columns = ['Sales', 'Expenses', 'Profit'];

  return (
    <div>
      <p>Select data for {chartType} Chart:</p>
      {columns.map(column => (
        <label key={column}>
          <input type="checkbox" value={column} onChange={onDataSelect} />
          {column}
        </label>
      ))}
    </div>
  );
};

export default ChartDataSelector;
