import React from "react";
import { Typography } from "@mui/material";

function ChartSettings({ selectedChartType }) {

    const renderChartTypeSettings = () => {
        // Based on the selected chart type, render specific settings
        // This is a placeholder, you'll need to implement the logic based on your requirements
        switch (selectedChartType) {
            case 'bar':
                return <Typography>Bar Chart Settings</Typography>;
            case 'line':
                return <Typography>Line Chart Settings</Typography>;
            case 'pie':
                return <Typography>Pie Chart Settings</Typography>;
            default:
                return <Typography>Select a chart type to configure settings</Typography>;
        }
    };

    return(
        <div>
            {renderChartTypeSettings()}
        </div>
    )
}

export default ChartSettings