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
import FileUploader from "./FileUploader";
import DataPreviewAndFormatEditor from "./DataPreviewAndFormatEditor";
import {
  getPreviewData,
  getAvailableColumnTypes,
  getSuggestedColumnMetadata,
} from "../../api/dataProfilesRequests";

function CreateDataProfileWindow({ open, onClose, onCreate }) {
  const [name, setName] = useState("");
  const [extractInstructions, setExtractInstructions] = useState("");
  const [sampleFiles, setSampleFiles] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [availableColumnTypes, setAvailableColumnTypes] = useState([]);
  const [columnMetadata, setColumnMetadata] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [isPreviewTableOpen, setIsPreviewTableOpen] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    onCreate(name, extractInstructions, columnMetadata);
  };

  const handlePreview = () => {
    if (sampleFiles.length && extractInstructions) {
      setIsPreviewLoading(true);
      setPreviewData(null);
      setColumnMetadata(null);

      const formData = new FormData();
      sampleFiles.forEach((file) => {
        formData.append("files", file);
      });
      formData.append("extract_instructions", extractInstructions);

      Promise.all([
        getPreviewData(sampleFiles, extractInstructions),
        getAvailableColumnTypes(),
      ])
        .then(([previewDataResponse, availableTypesResponse]) => {
          setPreviewData(previewDataResponse.data);
          setAvailableColumnTypes(availableTypesResponse.data);

          return getSuggestedColumnMetadata(previewDataResponse.data);
        })
        .then((suggestedTypesResponse) => {
          setColumnMetadata(suggestedTypesResponse.data);
          setIsPreviewTableOpen(true);
        })
        .catch((error) => {
          console.error("Error during preview setup:", error);
        })
        .finally(() => {
          setIsPreviewLoading(false);
        });
    }
  };

  return (
    <Dialog
      open={open}
      onClose={() => {
        onClose();
        setName(""); // Reset name
        setExtractInstructions(""); // Reset extractInstructions
        setSampleFiles([]); // Reset sampleFiles
        setPreviewData(null); // Reset previewData
      }}
      maxWidth="md"
      fullWidth
    >
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
            {previewData && columnMetadata && (
              <DataPreviewAndFormatEditor
                previewData={previewData}
                setPreviewData={setPreviewData}
                availableColumnTypes={availableColumnTypes}
                columnMetadata={columnMetadata}
                setColumnMetadata={setColumnMetadata}
              />
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
