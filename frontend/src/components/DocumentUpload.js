import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Button, Box, Typography, Paper } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const DocumentUpload = ({ onUpload, disabled }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    disabled: disabled,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onUpload(acceptedFiles[0]);
      }
    }
  });

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <div {...getRootProps()} style={{
        border: '2px dashed #1976d2',
        borderRadius: '4px',
        padding: '40px 20px',
        textAlign: 'center',
        cursor: disabled ? 'not-allowed' : 'pointer',
        backgroundColor: isDragActive ? '#e3f2fd' : '#fafafa',
        opacity: disabled ? 0.7 : 1,
      }}>
        <input {...getInputProps()} />
        <CloudUploadIcon fontSize="large" color="primary" />
        <Typography variant="h6" gutterBottom>
          {isDragActive ? 'Drop document here' : 'Drag & drop document or click to browse'}
        </Typography>
        <Typography variant="body1" color="textSecondary" gutterBottom>
          Supported formats: PDF, PNG, JPG (Max size: 10MB)
        </Typography>
        <Button 
          variant="contained" 
          color="primary"
          disabled={disabled}
        >
          Select File
        </Button>
      </div>
    </Paper>
  );
};

export default DocumentUpload;