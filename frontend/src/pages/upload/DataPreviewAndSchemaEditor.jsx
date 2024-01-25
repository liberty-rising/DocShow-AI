import React, { useState, useEffect, useRef } from "react";
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
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";

function DataPreviewAndSchemaEditor({ previewData }) {
  const data = Array.isArray(previewData) ? previewData : [previewData];
  const [columnNames, setColumnNames] = useState([]);
  const [columnTypes, setColumnTypes] = useState([]);
  const [editingColumnIndex, setEditingColumnIndex] = useState(null);
  const inputRefs = useRef([]);

  useEffect(() => {
    if (data && data.length > 0) {
      const newColumnNames = Object.keys(data[0]);
      const newColumnTypes = newColumnNames.map(() => "string");
      if (JSON.stringify(newColumnNames) !== JSON.stringify(columnNames)) {
        setColumnNames(newColumnNames);
      }
      if (JSON.stringify(newColumnTypes) !== JSON.stringify(columnTypes)) {
        setColumnTypes(newColumnTypes);
      }
    }
  }, [data]);

  const generateHeaderRow = (data) => {
    if (data && data.length > 0) {
      return columnNames.map((key, index) => (
        <TableCell key={index}>
          <TextField
            defaultValue={key.replace(/_/g, " ").toUpperCase()}
            onChange={(event) =>
              handleColumnNameChange(index, event.target.value)
            }
            variant="standard"
            InputProps={{
              disableUnderline: true,
              readOnly: editingColumnIndex !== index,
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => handleEditClick(index)}>
                    <EditIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }}
            inputRef={(ref) => (inputRefs.current[index] = ref)}
            onClick={() => handleEditClick(index)}
            style={{ cursor: "pointer" }}
            inputProps={{
              style: {
                cursor: editingColumnIndex === index ? "text" : "pointer",
              },
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                setEditingColumnIndex(null);
              }
            }}
          />
          <Select
            value={columnTypes[index]}
            onChange={(event) =>
              handleColumnTypeChange(index, event.target.value)
            }
          >
            <MenuItem value={"string"}>String</MenuItem>
            <MenuItem value={"number"}>Number</MenuItem>
            <MenuItem value={"boolean"}>Boolean</MenuItem>
            <MenuItem value={"date"}>Date</MenuItem>
            // Add more MenuItem components for other data types as needed
          </Select>
        </TableCell>
      ));
    }
  };

  const handleColumnTypeChange = (index, newType) => {
    setColumnTypes((prevColumnTypes) => {
      const newColumnTypes = [...prevColumnTypes];
      newColumnTypes[index] = newType;
      return newColumnTypes;
    });
  };

  const handleEditClick = (index) => {
    setEditingColumnIndex(index);
    inputRefs.current[index].select();
  };

  const handleColumnNameChange = (index, newName) => {
    setColumnNames((prevColumnNames) => {
      const newColumnNames = [...prevColumnNames];
      newColumnNames[index] = newName;
      return newColumnNames;
    });
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>{generateHeaderRow(data)}</TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
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

export default DataPreviewAndSchemaEditor;
