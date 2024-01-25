import React, { useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  Stack,
  TextField,
} from "@mui/material";
import axios from "axios";
import FileUploader from "./FileUploader";
import DataPreviewAndSchemaEditor from "./DataPreviewAndSchemaEditor";
import { API_URL } from "../../utils/constants";

function CreateDataProfileWindow({ open, onClose, onCreate }) {
  const [name, setName] = useState("");
  const [extractInstructions, setExtractInstructions] = useState("");
  const [sampleFiles, setSampleFiles] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [isPreviewTableOpen, setIsPreviewTableOpen] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    onCreate(name, extractInstructions);
  };

  const handlePreview = () => {
    if (sampleFiles.length && extractInstructions) {
      setIsPreviewLoading(true);
      const formData = new FormData();
      sampleFiles.forEach((file) => {
        formData.append("files", file); // Append each file
      });
      formData.append("extract_instructions", extractInstructions);

      axios
        .post(`${API_URL}data-profiles/preview/`, formData, {
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

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Create a Data Profile</DialogTitle>
      <DialogContent>
        <form onSubmit={handleSubmit}>
          <Box mt={2}>
            <TextField
              label="What would you like to name this data profile?"
              value={name}
              onChange={(e) => setName(e.target.value)}
              fullWidth
            />
          </Box>
          <Box mt={2}>
            <FileUploader
              setFiles={setSampleFiles}
              id="create-data-profile-uploader"
            />
          </Box>
          <Box mt={2}>
            <TextField
              label="What would you like to extract from the data?"
              value={extractInstructions}
              onChange={(e) => setExtractInstructions(e.target.value)}
              fullWidth
              multiline
              disabled={isPreviewLoading}
            />
          </Box>
          <Box mt={2}>
            {previewData && (
              <DataPreviewAndSchemaEditor previewData={previewData} />
            )}
          </Box>
          <Box display="flex" justifyContent="center" mt={2}>
            {isPreviewLoading && <CircularProgress />}
          </Box>
          <Stack direction="row" spacing={2} mt={2} alignItems={"center"}>
            <Button
              variant="contained"
              color="info"
              onClick={handlePreview}
              disabled={
                !sampleFiles || !extractInstructions || isPreviewLoading
              }
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  event.preventDefault();
                }
              }}
            >
              Preview
            </Button>
            <Button
              type="submit"
              color="primary"
              variant="contained"
              disabled={!isPreviewTableOpen || !name || !extractInstructions}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  event.preventDefault();
                }
              }}
            >
              Create
            </Button>
          </Stack>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default CreateDataProfileWindow;
