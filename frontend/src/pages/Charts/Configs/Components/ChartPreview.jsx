import React from "react";
import { Box, Typography } from "@mui/material";
import BarChartComponent from "../../Components/BarChart";

function ChartPreview({ chartConfig }) {
    // Render the chart based on chartConfig
    switch (chartConfig.type) {
        case 'bar':
            return <BarChartComponent chartConfig={chartConfig} />;
        case 'line':
            return <Typography>Line Chart</Typography>;
        case 'pie':
            return <Typography>Pie Chart</Typography>;
        default:
            return <Typography>Configure a chart to view it</Typography>;
    }
}

export default ChartPreview