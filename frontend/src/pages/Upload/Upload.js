import React, { useState, useEffect } from 'react';
import { Box, Button, Stack, Typography } from '@mui/material';
import axios from 'axios';
import FileTypeSelector from './FileTypeSelector';
import EncodingSelector from './EncodingSelector';
import DescriptionField from './DescriptionField';
import NewTableSelector from './NewTableSelector';
import FileUploader from './FileUploader';
import AlertSnackbar from './AlertSnackbar';
import { API_URL } from '../../utils/constants';

function UploadPage() {
  const [fileTypes, setFileTypes] = useState([]);
  const [encodings, setEncodings] = useState([]);
  const [fileType, setFileType] = useState('');
  const [encoding, setEncoding] = useState('');
  const [description, setDescription] = useState('');
  const [isNewTable, setIsNewTable] = useState('no');
  const [file, setFile] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);
  const [alertInfo, setAlertInfo] = useState({ open: false, message: '', severity: 'info' });

  useEffect(() => {
    // Fetch file types
    axios.get(`${API_URL}file_types/`)
      .then(response => setFileTypes(response.data))
      .catch(error => console.error('Error fetching file types', error));
  }, []);

  useEffect(() => {
    if (fileType === 'csv') {
      // Fetch encodings
      axios.get(`${API_URL}encodings/`, { params: { file_type: fileType } })
        .then(response => setEncodings(response.data))
        .catch(error => console.error('Error fetching encodings', error));
    }
  }, [fileType]);

  const handleAnalyze = () => {
    // Placeholder for analyze functionality
    setAnalyzed(true);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('extra_desc', description);
    formData.append('is_new_table', isNewTable === 'yes');
    formData.append('encoding', encoding);

    try {
      const response = await axios.post(`${API_URL}upload/`, formData);
      if (response.status === 200) {
        setAlertInfo({ open: true, message: 'File uploaded successfully!', severity: 'success' });
      } else {
        setAlertInfo({ open: true, message: `Failed to upload file: ${response.statusText}`, severity: 'error' });
      }
    } catch (error) {
      setAlertInfo({ open: true, message: `An error occurred: ${error.message}`, severity: 'error' });
    }
  };

  const handleCloseSnackbar = () => {
    setAlertInfo({ ...alertInfo, open: false });
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, marginBottom: 2 }}>
        <Typography variant="h4" gutterBottom>📥 Data Upload</Typography>
      </Box>

      <FileTypeSelector fileTypes={fileTypes} fileType={fileType} setFileType={setFileType} />
      
      {fileType === 'csv' && (
        <EncodingSelector encodings={encodings} encoding={encoding} setEncoding={setEncoding} />
      )}

      <DescriptionField description={description} setDescription={setDescription} />

      <NewTableSelector isNewTable={isNewTable} setIsNewTable={setIsNewTable} />

      <FileUploader fileType={fileType} setFile={setFile} />

      <Stack direction="row" spacing={2} mt={2}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleAnalyze}
          disabled={!file}
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

export default UploadPage
