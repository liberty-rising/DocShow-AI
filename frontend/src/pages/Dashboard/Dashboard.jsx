import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { API_URL } from '../../utils/constants';

function Dashboard() {
  const { dashboardId } = useParams();
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // Ensure organization is not empty and dashboardId is available
    if (dashboardId) {
      fetch(`${API_URL}/dashboard/?id=${dashboardId}`)
        .then(response => response.json())
        .then(data => setDashboardData(data))
        .catch(error => console.error('Error fetching dashboard:', error));
    }
  }, [dashboardId]);

  if (!dashboardData) return <div>Loading...</div>;

  return (
    <div>
      <h2>{dashboardData.name}</h2>
      {/* Render your dashboard data here */}
    </div>
  );
}

export default Dashboard;
