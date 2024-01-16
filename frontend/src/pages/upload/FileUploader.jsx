import React from "react";
import { Button } from "@mui/material";

const FileUploader = ({ fileType, setFile }) => {
  const fileAcceptType = fileType === "csv" ? ".csv" : ""; // Adjust this logic based on your file types

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  return (
    <div>
      <input
        accept={fileAcceptType}
        type="file"
        id="contained-button-file"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <label htmlFor="contained-button-file">
        <Button variant="contained" color="primary" component="span">
          Upload File
        </Button>
      </label>
    </div>
  );
};

export default FileUploader;
