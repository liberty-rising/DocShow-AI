import React from "react";
import BarChartComponent from "./components/BarChart";
import LineChartComponent from "./components/LineChart";
import PieChartComponent from "./components/PieChart";

const ChartDisplay = ({ chartType, config }) => {
  switch (chartType) {
    case "bar":
      return <BarChartComponent chartConfig={config} />;
    case "line":
      return <LineChartComponent config={config} />;
    case "pie":
      return <PieChartComponent config={config} />;
    default:
      return <p>Select a chart type</p>;
  }
};

export default ChartDisplay;
