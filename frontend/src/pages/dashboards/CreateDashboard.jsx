import React, { useState, useEffect } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../../utils/constants";

const CreateDashboardPage = () => {
  const [organization, setOrganization] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch organization
    axios
      .get(`${API_URL}users/me/`)
      .then((response) => {
        setOrganization(response.data.organization);
      })
      .catch((error) => console.error("Error fetching organization:", error));
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    axios
      .post(`${API_URL}dashboard/`, { name, description, organization })
      .then((response) => {
        // Handle successful dashboard creation
        console.log("Dashboard created:", response.data);
        navigate("/dashboards");
      })
      .catch((error) => {
        console.error("Error creating dashboard:", error);
      });
  };

  const handleBack = () => {
    navigate("/dashboards");
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
      <Typography variant="h6">Create New Dashboard</Typography>
      <TextField
        required
        fullWidth
        label="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        margin="normal"
      />
      <TextField
        required
        fullWidth
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        margin="normal"
      />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        Create Dashboard
      </Button>
      <Button fullWidth variant="outlined" sx={{ mt: 1 }} onClick={handleBack}>
        Back to Dashboards
      </Button>
    </Box>
  );
};

export default CreateDashboardPage;
