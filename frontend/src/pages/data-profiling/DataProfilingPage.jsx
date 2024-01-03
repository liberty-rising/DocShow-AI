import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
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
  TextField
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../../utils/constants';

function DataProfilingPage() {
  const [dataProfiles, setDataProfiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState('');
  const [instructions, setInstructions] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [previewData, setPreviewData] = useState(null); 
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  useEffect(() => {
    axios.get(`${API_URL}data-profiles/`)
      .then(response => {
        if (Array.isArray(response.data)) {
          setDataProfiles(response.data);
        } else {
          console.error('Received data is not an array:', response.data);
          setDataProfiles([]);
        }
      })
      .catch(error => console.error('Error fetching data profiles:', error));
  }, []);

  const handleProfileCreate = () => {
    navigate('/data-profiling/create');
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setSelectedFileName(file.name);
    }
  };

  const handleInstructionsChange = (event) => {
    setInstructions(event.target.value);
  };

  const handleUpload = () => {
    if (selectedFile) {
      setIsUploading(true);
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('instructions', instructions);

      axios.post(`${API_URL}upload-url`, formData)
        .then(response => {
          console.log(response);
          setIsUploading(false);
          // Reset states after upload
          setSelectedFile(null);
          setSelectedFileName('');
          setInstructions('');
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          setIsUploading(false);
        });
    }
  };

  const handlePreview = () => {
    if (selectedFile && instructions) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('instructions', instructions);

      axios.post(`${API_URL}data-profiles/preview-endpoint/`, formData, { 
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          setPreviewData(response.data); // Store the preview data
        })
        .catch(error => console.error('Error on preview:', error));
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>🔍 Data Profiling</Typography>
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
          sx={{ bgcolor: isUploading ? 'secondary.main' : 'grey.500' }}
        >
          Upload File
        </Button>

        <Button
          variant="contained"
          color="info"
          onClick={handlePreview}
          disabled={!selectedFile || !instructions} // Disable if no file or instructions
        >
          Preview
        </Button>

        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
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

      {selectedFileName && (
        <Typography variant="subtitle1" gutterBottom>
          File selected: {selectedFileName}
        </Typography>
      )}

      {/* Display preview data if available */}
      {previewData && (
        <Typography variant="subtitle1" gutterBottom>
          Preview Data: {JSON.stringify(previewData)}
        </Typography>
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
                  <Link component="button" variant="body2" onClick={() => handleProfileClick(profile.id)}>
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
