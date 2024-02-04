import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Tooltip,
} from "@mui/material";
import { format } from "date-fns";
import { API_URL } from "../../utils/constants";
import axios from "axios";

function DashboardTable() {
  const [reports, setReports] = useState([]);

  console.log("reports", reports);

  useEffect(() => {
    axios
      .get(`${API_URL}powerbi/reports/`)
      .then((response) => setReports(response.data.reports.value))
      .catch((error) => console.error("Error fetching reports:", error));
  }, []);

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Description</TableCell>
          <TableCell>Created at</TableCell>
          <TableCell>Updated at</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {reports.length > 0 &&
          reports.map((report) => (
            <TableRow key={report.name} hover>
              <TableCell>
                <a
                  href={`https://app.powerbi.com/reportEmbed?reportId=${report.id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {report.name}
                </a>
              </TableCell>
              <TableCell
                style={{
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                <Tooltip title={report.description} placement="top">
                  <div>{report.description}</div>
                </Tooltip>
              </TableCell>
              <TableCell>
                {report.created_at
                  ? format(new Date(report.created_at), "yyyy-MM-dd")
                  : "N/A"}
              </TableCell>
              <TableCell>
                {report.updated_at
                  ? format(new Date(report.updated_at), "yyyy-MM-dd")
                  : "N/A"}
              </TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}

export default DashboardTable;
