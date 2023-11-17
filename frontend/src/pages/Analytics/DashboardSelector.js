// DashboardSelector.js
import React from 'react';

const DashboardSelector = ({ onSelectDashboard }) => {
  // This could be loaded from an API
  const dashboards = ['Dashboard 1', 'Dashboard 2'];

  return (
    <select onChange={(e) => onSelectDashboard(e.target.value)}>
      {dashboards.map(dashboard => (
        <option key={dashboard} value={dashboard}>{dashboard}</option>
      ))}
      <option value="new">Create New Dashboard</option>
    </select>
  );
};

export default DashboardSelector;
