import React, { useState, useEffect } from "react";
import {
  Box,
  IconButton,
  InputAdornment,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";

function DataPreviewAndSchemaEditor({
  previewData,
  availableColumnTypes,
  selectedColumnTypes,
  onColumnsChange,
}) {
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    if (Array.isArray(previewData) && previewData.length > 0) {
      const initialColumns = Object.keys(previewData[0]).map((key) => ({
        name: key,
        type: selectedColumnTypes[key] || "text",
        isEditing: false,
      }));
      setColumns(initialColumns);
    }
  }, [previewData, selectedColumnTypes]);

  useEffect(() => {
    onColumnsChange(columns); // Call the callback function when columns change
  }, [columns]);

  const handleColumnTypeChange = (index, newType) => {
    setColumns((prevColumns) =>
      prevColumns.map((column, colIndex) =>
        colIndex === index ? { ...column, type: newType } : column,
      ),
    );
  };

  const handleEditClick = (index) => {
    setColumns((prevColumns) =>
      prevColumns.map((column, colIndex) =>
        colIndex === index
          ? { ...column, isEditing: !column.isEditing }
          : column,
      ),
    );
  };

  const handleColumnNameChange = (index, newName) => {
    setColumns((prevColumns) =>
      prevColumns.map((column, colIndex) =>
        colIndex === index ? { ...column, name: newName } : column,
      ),
    );
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            {columns.map((column, index) => (
              <TableCell key={index}>
                <TextField
                  defaultValue={column.name.replace(/_/g, " ").toUpperCase()}
                  onChange={(event) =>
                    handleColumnNameChange(index, event.target.value)
                  }
                  variant="standard"
                  InputProps={{
                    disableUnderline: true,
                    readOnly: !column.isEditing,
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={() => handleEditClick(index)}>
                          <EditIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  style={{ cursor: "pointer" }}
                />
                <Tooltip title="Select the format of this column">
                  <Select
                    fullWidth
                    value={
                      availableColumnTypes.includes(column.type)
                        ? column.type
                        : ""
                    }
                    onChange={(event) =>
                      handleColumnTypeChange(index, event.target.value)
                    }
                  >
                    {availableColumnTypes.map((type) => (
                      <MenuItem value={type} key={type}>
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                      </MenuItem>
                    ))}
                  </Select>
                </Tooltip>
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {previewData.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {Object.values(row).map((value, cellIndex) => (
                <TableCell key={cellIndex}>{value}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default DataPreviewAndSchemaEditor;
