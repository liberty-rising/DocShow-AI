import React from "react";
import { Box, Typography } from "@mui/material";
import { ResponsivePie } from "@nivo/pie";

const PieChartComponent = ({ config }) => (
  <Box>
    <Typography variant="h6" gutterBottom>
      {config.title}
    </Typography>
    <div style={{ height: "400px" }}>
      <ResponsivePie data={config.data} />
    </div>
  </Box>
);

export default PieChartComponent;
