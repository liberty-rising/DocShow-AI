import React from "react";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

function PreviewTable({ previewData }) {
  const generateTableHeaders = (data) => {
    if (data && data.length > 0) {
      return Object.keys(data[0]).map((key) => (
        <TableCell key={key}>{key.replace(/_/g, " ").toUpperCase()}</TableCell>
      ));
    }
    return null;
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>{generateTableHeaders(previewData)}</TableRow>
        </TableHead>
        <TableBody>
          {previewData.map((row, index) => (
            <TableRow key={index}>
              {Object.values(row).map((value, idx) => (
                <TableCell key={idx}>{value}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default PreviewTable;
