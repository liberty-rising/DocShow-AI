import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Link,
  Button,
  TextField,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../../utils/constants";

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const [instructions, setInstructions] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [previewData, setPreviewData] = useState(null);
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [selectedFiles, setSelectedFiles] = useState([]); // Array of files
  const [selectedFileNames, setSelectedFileNames] = useState([]); // Array of file names

  useEffect(() => {
    axios
      .get(`${API_URL}data-profiles/`)
      .then((response) => {
        if (Array.isArray(response.data)) {
          setDataProfiles(response.data);
        } else {
          console.error("Received data is not an array:", response.data);
          setDataProfiles([]);
        }
      })
      .catch((error) => console.error("Error fetching data profiles:", error));
  }, []);

  const generateTableHeaders = (data) => {
    if (data && data.length > 0) {
      return Object.keys(data[0]).map((key) => (
        <TableCell key={key}>{key.replace(/_/g, " ").toUpperCase()}</TableCell>
      ));
    }
    return null;
  };

  const handleProfileCreate = () => {
    navigate("/data-profiling/create");
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    if (files.length) {
      setSelectedFiles(files);
      setSelectedFileNames(files.map((file) => file.name));
    }
  };

  const handleInstructionsChange = (event) => {
    setInstructions(event.target.value);
  };

  const handleUpload = () => {
    if (selectedFiles.length) {
      setIsUploading(true);
      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file); // Append each file to the form data
      });
      formData.append("instructions", instructions);

      axios
        .post(`${API_URL}upload-url`, formData)
        .then((response) => {
          console.log(response);
          setIsUploading(false);
          // Reset states after upload
          setSelectedFiles([]);
          setSelectedFileNames([]);
          setInstructions("");
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
          setIsUploading(false);
        });
    }
  };

  const handlePreview = () => {
    if (selectedFiles.length && instructions) {
      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file); // Append each file
      });
      formData.append("instructions", instructions);

      axios
        .post(`${API_URL}data-profiles/preview/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          setPreviewData(response.data); // Store the preview data
        })
        .catch((error) => console.error("Error on preview:", error));
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🔍 Data Profiling
      </Typography>
      <Box display="flex" justifyContent="space-between" mb={2}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleProfileCreate}
        >
          Create New Data Profile
        </Button>

        <Button
          variant="contained"
          onClick={handleUploadClick}
          disabled={isUploading}
          sx={{ bgcolor: isUploading ? "secondary.main" : "grey.500" }}
        >
          Upload File
        </Button>

        <Button
          variant="contained"
          color="info"
          onClick={handlePreview}
          disabled={!selectedFiles || !instructions} // Disable if no file or instructions
        >
          Preview
        </Button>

        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          multiple // Allow multiple file selection
          style={{ display: "none" }}
        />
      </Box>

      <TextField
        label="Instructions"
        variant="outlined"
        fullWidth
        margin="normal"
        value={instructions}
        onChange={handleInstructionsChange}
        helperText="Write any special instructions here"
      />

      {selectedFileNames.length > 0 && (
        <Typography variant="subtitle1" gutterBottom>
          Files selected: {selectedFileNames.join(", ")}
        </Typography>
      )}

      {/* Display preview data if available */}
      {previewData && (
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
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dataProfiles.map((profile) => (
              <TableRow key={profile.id}>
                <TableCell>
                  <Link
                    component="button"
                    variant="body2"
                    onClick={() => handleProfileClick(profile.id)}
                  >
                    {profile.name}
                  </Link>
                </TableCell>
                <TableCell>{profile.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default DataProfilingPage;
