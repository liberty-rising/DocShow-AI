import React from "react";
import { Typography } from "@mui/material";
import BarChartComponent from "../../BarChart";

function ChartPreviewForm({ chartConfig }) {
  switch (selectedChartType) {
    case "bar":
      return <BarChartComponent config={chartConfig} />;
    case "line":
      return <Typography>Line Chart</Typography>;
    case "pie":
      return <Typography>Pie Chart</Typography>;
    default:
      return <Typography>Configure a chart to view it</Typography>;
  }
}

export default ChartPreviewForm;
