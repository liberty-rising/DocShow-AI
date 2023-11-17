import React from 'react';
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

const FileTypeSelector = ({ fileTypes, fileType, setFileType }) => (
  <FormControl component="fieldset">
    <FormLabel component="legend">Choose file type</FormLabel>
    <RadioGroup row value={fileType} onChange={(e) => setFileType(e.target.value)}>
      {fileTypes.map((type, index) => (
        <FormControlLabel key={index} value={type} control={<Radio />} label={type.toUpperCase()} />
      ))}
    </RadioGroup>
  </FormControl>
);

export default FileTypeSelector;
