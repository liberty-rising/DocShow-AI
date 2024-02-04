import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { API_URL } from "../../utils/constants";
import * as pbi from "powerbi-client";

function ReportPage() {
  const { report_id } = useParams();
  const [token, setToken] = useState("");
  const [report, setReport] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_URL}powerbi/token/`)
      .then((response) => setToken(response.data.token))
      .catch((error) => console.error("Error fetching token:", error));

    axios
      .get(`${API_URL}powerbi/reports/${report_id}`)
      .then((response) => setReport(response.data.report))
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

      const powerbi = new pbi.service.Service(
        pbi.factories.hpmFactory,
        pbi.factories.wpmpFactory,
        pbi.factories.routerFactory,
      );
      const reportContainer = document.getElementById("reportContainer");
      powerbi.embed(reportContainer, config);
    }
  }, [report, token]);

  return (
    <div id="reportContainer">
      {/* The Power BI report will be embedded here */}
    </div>
  );
}

export default ReportPage;
