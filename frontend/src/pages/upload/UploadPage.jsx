import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import axios from "axios";
import AlertSnackbar from "./AlertSnackbar";
import CreateDataProfilePage from "./CreateDataProfilePage";
import DataProfileSelector from "./DataProfileSelector";
import FileUploader from "./FileUploader";
import PreviewTable from "./PreviewTable";
import { API_URL } from "../../utils/constants";

function UploadPage() {
  const [files, setFiles] = useState([]);
  const [dataProfile, setDataProfile] = useState(null);
  const [dataProfiles, setDataProfiles] = useState([]);
  const [alertInfo, setAlertInfo] = useState({
    open: false,
    message: "",
    severity: "info",
  });
  const [showCreateDataProfile, setShowCreateDataProfile] = useState(false);
  const [previewData, setPreviewData] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [isPreviewTableOpen, setIsPreviewTableOpen] = useState(false);

  useEffect(() => {
    axios
      .get(`${API_URL}data-profiles/org/`)
      .then((response) => {
        setDataProfiles(response.data);
      })
      .catch((error) => console.error("Error fetching data profiles:", error));
  }, []);

  const handleCreateDataProfile = (name, extractInstructions) => {
    axios
      .post(`${API_URL}data-profile/`, {
        name: name,
        description: extractInstructions,
      })
      .then((response) => {
        // Handle successful data profile creation
        setDataProfiles((prevDataProfiles) => [...prevDataProfiles, name]);
        setShowCreateDataProfile(false);
      })
      .catch((error) => {
        console.error("Error creating data profile:", error);
      });
  };

  const handlePreview = () => {
    if (files.length && dataProfile) {
      setIsPreviewLoading(true);
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file); // Append each file
      });

      axios
        .post(`${API_URL}data-profiles/${dataProfile}/preview/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          setPreviewData(response.data); // Store the preview data
          setIsPreviewTableOpen(true);
          setIsPreviewLoading(false);
        })
        .catch((error) => {
          console.error("Error on preview:", error);
          setIsPreviewLoading(false);
        });
    }
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

      <Stack direction="row" spacing={2} alignItems="center">
        <DataProfileSelector
          dataProfiles={dataProfiles}
          dataProfile={dataProfile}
          setDataProfile={setDataProfile}
        />
        <Button
          onClick={() => setShowCreateDataProfile(true)}
          variant="contained"
          color="primary"
        >
          Create a data profile
        </Button>
        <CreateDataProfilePage
          open={showCreateDataProfile}
          onClose={() => setShowCreateDataProfile(false)}
          onCreate={handleCreateDataProfile}
        />
      </Stack>

      <Box mt={2}>
        <FileUploader setFiles={setFiles} />
      </Box>

      <Box mt={2}>
        {previewData && <PreviewTable previewData={previewData} />}
      </Box>
      <Box display="flex" justifyContent="center" mt={2}>
        {isPreviewLoading && <CircularProgress />}
      </Box>

      <Stack direction="row" spacing={2} mt={2}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handlePreview}
          disabled={!files.length || !dataProfile || isPreviewLoading}
        >
          Preview
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={
            !files ||
            !dataProfile ||
            !previewData ||
            !isPreviewTableOpen ||
            isPreviewLoading
          }
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
