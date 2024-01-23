import React, { useState } from "react";
import { Box, Typography, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

const FileUploader = ({ setFiles, id }) => {
  const [fileNames, setFileNames] = useState([]);
  const [fileType, setFileType] = useState(null);

  const handleFileChange = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    const uploadedFileType = uploadedFiles[0].type;
    if (uploadedFiles.some((file) => file.type !== uploadedFileType)) {
      alert("All files must be of the same type.");
    } else if (fileType && uploadedFileType !== fileType) {
      alert("All files must be of the same type as previously uploaded files.");
    } else {
      if (fileNames.length + uploadedFiles.length > 5) {
        alert("You can only upload a maximum of 5 files.");
      } else {
        if (!fileType) {
          setFileType(uploadedFileType);
        }
        setFiles((prevFiles) => [...prevFiles, ...uploadedFiles]);
        setFileNames((prevNames) => [
          ...prevNames,
          ...uploadedFiles.map((file) => file.name),
        ]);
      }
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const uploadedFiles = Array.from(event.dataTransfer.files);
    const uploadedFileType = uploadedFiles[0].type;
    if (uploadedFiles.some((file) => file.type !== uploadedFileType)) {
      alert("All files must be of the same type.");
    } else if (fileType && uploadedFileType !== fileType) {
      alert("All files must be of the same type as previously uploaded files.");
    } else {
      if (fileNames.length + uploadedFiles.length > 5) {
        alert("You can only upload a maximum of 5 files.");
      } else {
        if (!fileType) {
          setFileType(uploadedFileType);
        }
        setFiles((prevFiles) => [...prevFiles, ...uploadedFiles]);
        setFileNames((prevNames) => [
          ...prevNames,
          ...uploadedFiles.map((file) => file.name),
        ]);
      }
    }
  };

  const handleDelete = (indexToDelete) => {
    setFileNames(fileNames.filter((_, index) => index !== indexToDelete));
    setFiles((prevFiles) =>
      Array.from(prevFiles).filter((_, index) => index !== indexToDelete),
    );
    if (fileNames.length === 1) {
      setFileType(null);
    }
  };

  return (
    <Box
      sx={{
        height: 200,
        width: "100%",
        border: "2px dashed",
        borderColor: "divider",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
      }}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id={id}
        style={{ display: "none" }}
        onChange={handleFileChange}
        multiple
      />
      <label htmlFor={id}>
        <Typography variant="body1" component="span">
          {fileNames.length === 0
            ? "Drag 'n' drop some files here, or click to select files"
            : "Click to select more files"}
        </Typography>
      </label>
      {fileNames.map((name, index) => (
        <Box key={index} sx={{ display: "flex", alignItems: "center" }}>
          <Typography variant="body2">{name}</Typography>
          <IconButton onClick={() => handleDelete(index)} size="small">
            <DeleteIcon />
          </IconButton>
        </Box>
      ))}
    </Box>
  );
};

export default FileUploader;
