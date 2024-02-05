import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  IconButton,
} from "@mui/material";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";

function EditableCell({
  value: initialValue,
  row: index,
  column: id,
  updateMyData,
}) {
  const [value, setValue] = useState(initialValue);

  const onChange = (e) => {
    setValue(e.target.value);
  };

  const onBlur = () => {
    updateMyData(index, id, value);
  };

  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  return (
    <TextField fullWidth value={value} onChange={onChange} onBlur={onBlur} />
  );
}

function ResizableColumn({ children, onResize }) {
  const [width, setWidth] = useState(150);

  const handleMouseDown = (e) => {
    e.preventDefault();
    const startX = e.pageX;
    const startWidth = width;

    const doResize = (moveE) => {
      const newWidth = startWidth + moveE.pageX - startX;
      setWidth(newWidth);
      onResize(newWidth);
    };

    const stopResize = () => {
      document.removeEventListener("mousemove", doResize);
      document.removeEventListener("mouseup", stopResize);
    };

    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
  };

  return (
    <TableCell style={{ width: `${width}px` }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        <span>{children}</span>
        <IconButton size="small" onMouseDown={handleMouseDown}>
          <DragIndicatorIcon />
        </IconButton>
      </div>
    </TableCell>
  );
}

function PreviewTableTest({ columnNames, previewData, onChangePreviewData }) {
  const columns = columnNames.map((name) => ({
    Header: name.toUpperCase(),
    accessor: name,
  }));

  const data = previewData || [];

  const updateMyData = (rowIndex, columnId, value) => {
    onChangePreviewData(rowIndex, columnId, value);
  };

  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            {columns.map((column, i) =>
              i !== columns.length - 1 ? (
                <ResizableColumn
                  key={i}
                  onResize={(newWidth) => console.log(`New width: ${newWidth}`)}
                >
                  {column.Header}
                </ResizableColumn>
              ) : (
                <TableCell key={i} style={{ width: `150px` }}>
                  {column.Header}
                </TableCell>
              ),
            )}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, i) => (
            <TableRow key={i}>
              {columns.map((column, j) => (
                <TableCell key={j}>
                  <EditableCell
                    value={row[column.accessor]}
                    row={i}
                    column={column.accessor}
                    updateMyData={updateMyData}
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

export default PreviewTableTest;
