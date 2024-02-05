import React, { useState, useEffect, useRef } from "react";
import {
  IconButton,
  InputAdornment,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextareaAutosize,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";

function EditableCell({ value, rowIndex, columnIndex, onEdit }) {
  const [editing, setEditing] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const inputRef = useRef(null);

  useEffect(() => {
    console.log(`EditableCell[${rowIndex}, ${columnIndex}]: value updated`);
    setInputValue(value);
  }, [value]);

  useEffect(() => {
    if (editing) {
      console.log(`EditableCell[${rowIndex}, ${columnIndex}]: focusing`);
      inputRef.current?.focus();
    }
  }, [editing]);

  const handleEdit = (e) => {
    console.log(`EditableCell[${rowIndex}, ${columnIndex}]: handleEdit`);
    setInputValue(e.target.value);
  };

  const handleBlur = () => {
    console.log(`EditableCell[${rowIndex}, ${columnIndex}]: handleBlur`);
    setEditing(false);
    onEdit(rowIndex, columnIndex, inputValue);
  };

  const toggleEdit = () => {
    console.log(`EditableCell[${rowIndex}, ${columnIndex}]: toggleEdit`);
    setEditing((edit) => !edit);
  };

  const handleClick = () => {
    console.log(`EditableCell[${rowIndex}, ${columnIndex}]: handleClick`);
    setEditing(true);
  };

  console.log(`EditableCell[${rowIndex}, ${columnIndex}]: rendering`);

  const commonStyle = {
    width: "100%", // Take full width of the cell
    border: "none", // No border
    fontSize: "inherit", // Ensure font size is consistent
    fontFamily: "inherit", // Match the font family
    resize: "none", // Disable resizing
    background: "transparent", // Transparent background
    outline: "none", // No outline on focus
  };

  return (
    <div
      onClick={handleClick}
      style={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        cursor: "text",
      }}
    >
      <TextareaAutosize
        readOnly={!editing}
        value={inputValue}
        onChange={handleEdit}
        onBlur={handleBlur}
        ref={inputRef}
        style={commonStyle}
        onClick={editing ? undefined : toggleEdit}
      />
    </div>
  );
}

function PreviewTable({ columnNames, previewData, onChangePreviewData }) {
  const handleChangeData = (rowIndex, columnIndex, newValue) => {
    onChangePreviewData((prevPreviewData) =>
      prevPreviewData.map((row, index) => {
        if (index === rowIndex) {
          return { ...row, [columnNames[columnIndex]]: newValue };
        }
        return row;
      }),
    );
  };

  return (
    <TableContainer component={Paper}>
      <Tooltip
        title="Preview the data based on the chosen data profile and data that you have uploaded"
        placement="top-start"
      >
        <Typography variant="h6" component="div" sx={{ padding: "1em" }}>
          Data Preview Table
        </Typography>
      </Tooltip>
      <Table sx={{ minWidth: 650, width: "100%" }}>
        <TableHead>
          <TableRow>
            {columnNames &&
              columnNames.map((columnName) => (
                <TableCell
                  key={columnName}
                  style={{ minWidth: "100px", width: "auto" }}
                >
                  {columnName.replace(/_/g, " ").toUpperCase()}
                </TableCell>
              ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {previewData &&
            previewData.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {Object.values(row).map((cellValue, columnIndex) => (
                  <TableCell
                    key={columnIndex}
                    style={{ minWidth: "100px", width: "auto" }}
                  >
                    <EditableCell
                      value={cellValue}
                      rowIndex={rowIndex}
                      columnIndex={columnIndex}
                      onEdit={handleChangeData}
                    />
                  </TableCell>
                ))}
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default PreviewTable;
