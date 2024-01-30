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

function PreviewTable({ columnNames, previewData }) {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            {columnNames &&
              columnNames.map((columnName) => (
                <TableCell key={columnName}>
                  {columnName.replace(/_/g, " ").toUpperCase()}
                </TableCell>
              ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {previewData &&
            previewData.map((row, index) => (
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
