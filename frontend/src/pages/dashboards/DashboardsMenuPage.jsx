import React from "react";
import { Box, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import DashboardTable from "./DashboardTable";

function DashboardMenuPage() {
  const navigate = useNavigate();

  const handleCreateDashboard = () => {
    navigate("/dashboards/create");
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        📊 Dashboards
      </Typography>
      <Button
        variant="contained"
        onClick={handleCreateDashboard}
        sx={{ mb: 2 }}
      >
        Create New Dashboard
      </Button>
      <DashboardTable />
    </Box>
  );
}

export default DashboardMenuPage;
