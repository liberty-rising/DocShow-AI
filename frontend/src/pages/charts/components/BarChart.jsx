import React from "react";
import { Box, Typography } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";

const BarChartComponent = ({ chartConfig }) => {
  const nivoBarConfig = chartConfig.nivoConfig || {}; // Ensure nivoConfig is not undefined

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {chartConfig.title}
      </Typography>
      <div style={{ height: "400px" }}>
        <ResponsiveBar {...nivoBarConfig} />
      </div>
    </Box>
  );
};

export default BarChartComponent;
