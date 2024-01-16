import React from "react";
import { Typography } from "@mui/material";
import BarConfig from "../BarConfig";

function ChartConfigForm({ selectedTable, selectedChartType, onConfigChange }) {
  switch (selectedChartType) {
    case "bar":
      return (
        <BarConfig
          selectedTable={selectedTable}
          onBarConfigChange={onConfigChange}
        />
      );
    case "line":
      return <Typography>Line Chart Settings</Typography>;
    case "pie":
      return <Typography>Pie Chart Settings</Typography>;
    default:
      return <Typography>Select a chart type to configure settings</Typography>;
  }
}

export default ChartConfigForm;
