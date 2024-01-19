import React, { useState, useEffect } from "react";
import { Box, Button, Stack, Typography } from "@mui/material";
import axios from "axios";
import AlertSnackbar from "./AlertSnackbar";
import DataProfileSelector from "./DataProfileSelector";
import { API_URL } from "../../utils/constants";

function UploadPage() {
  const [files, setFiles] = useState(null);
  const [dataProfile, setDataProfile] = useState([]);
  const [dataProfiles, setDataProfiles] = useState([]);
  const [analyzed, setAnalyzed] = useState(false);
  const [alertInfo, setAlertInfo] = useState({
    open: false,
    message: "",
    severity: "info",
  });

  useEffect(() => {
    axios
      .get(`${API_URL}data-profiles/org/`)
      .then((response) => {
        setDataProfiles(response.data);
      })
      .catch((error) => console.error("Error fetching data profiles:", error));
  }, []);

  const handleAnalyze = () => {
    // Placeholder for analyze functionality
    setAnalyzed(true);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", files);
    formData.append("extra_desc", description);
    formData.append("is_new_table", isNewTable === "yes");
    formData.append("encoding", encoding);

    try {
      const response = await axios.post(`${API_URL}upload/`, formData);
      if (response.status === 200) {
        setAlertInfo({
          open: true,
          message: "File uploaded successfully!",
          severity: "success",
        });
      } else {
        setAlertInfo({
          open: true,
          message: `Failed to upload file: ${response.statusText}`,
          severity: "error",
        });
      }
    } catch (error) {
      setAlertInfo({
        open: true,
        message: `An error occurred: ${error.message}`,
        severity: "error",
      });
    }
  };

  const handleCloseSnackbar = () => {
    setAlertInfo({ ...alertInfo, open: false });
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box
        sx={{ display: "flex", alignItems: "center", gap: 2, marginBottom: 2 }}
      >
        <Typography variant="h4" gutterBottom>
          📥 Data Upload
        </Typography>
      </Box>

      {/* <FileUploader fileType={fileType} setFile={setFile} /> */}

      <Stack direction="row" spacing={2} alignItems="center">
        <DataProfileSelector
          dataProfiles={dataProfiles}
          dataProfile={dataProfile}
          setDataProfile={setDataProfile}
        />
        <Button variant="contained" color="primary">
          Create a data profile
        </Button>
      </Stack>

      <Stack direction="row" spacing={2} mt={2}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleAnalyze}
          disabled={!files}
        >
          Analyze
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={!analyzed}
        >
          Submit
        </Button>
      </Stack>

      <AlertSnackbar
        open={alertInfo.open}
        handleClose={handleCloseSnackbar}
        severity={alertInfo.severity}
        message={alertInfo.message}
      />
    </Box>
  );
}

export default UploadPage;
