// AnalyticsPage.js
import React from "react";
import { Box, Typography, Grid } from "@mui/material";
import AIAssistant from "./AIAssistant";

function AIAnalystPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🤖 AI Analyst
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <AIAssistant />
        </Grid>
      </Grid>
    </Box>
  );
}

export default AIAnalystPage;
