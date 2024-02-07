import axios from "axios";
import * as pbi from "powerbi-client";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { API_URL } from "../../utils/constants";

function ReportPage() {
  const { report_id } = useParams();
  const [token, setToken] = useState("");
  const [report, setReport] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_URL}powerbi/reports/${report_id}`)
      .then((response) => {
        setReport(response.data.report);
        const report = response.data.report;
        const workspace_ids = [report.datasetWorkspaceId];
        const dataset_ids = [report.datasetId];
        const report_ids = [report.id];

        axios
          .post(`${API_URL}powerbi/embeded-token/`, {
            workspace_ids: workspace_ids,
            dataset_ids: dataset_ids,
            report_ids: report_ids,
          })
          .then((response) => {
            setToken(response.data.token);
          })
          .catch((error) => console.error("Error fetching token:", error));
      })
      .catch((error) => console.error("Error fetching report:", error));
  }, [report_id]);

  useEffect(() => {
    if (report && token) {
      const models = pbi.models;
      const config = {
        type: "report",
        tokenType: models.TokenType.Embed,
        accessToken: token,
        embedUrl: report.embedUrl,
        id: report.id,
        permissions: models.Permissions.All,
        settings: {
          filterPaneEnabled: true,
          navContentPaneEnabled: true,
        },
      };

      // Get a reference to the HTML element
      const reportContainer = document.getElementById("reportContainer");

      // Create a new instance of the PowerBi class
      const powerbi = new pbi.service.Service(
        pbi.factories.hpmFactory,
        pbi.factories.wpmpFactory,
        pbi.factories.routerFactory,
      );

      // Reset the Power BI container
      powerbi.reset(reportContainer);

      // Embed the report
      const embeddedReport = powerbi.embed(reportContainer, config);
    }
  }, [report, token]);

  return (
    <div id="reportContainer">
      {/* The Power BI report will be embedded here */}
    </div>
  );
}

export default ReportPage;
