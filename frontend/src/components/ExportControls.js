import React from 'react';
import { Button, ButtonGroup, Box } from '@mui/material';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

const ExportControls = ({ results, documentImage }) => {
  const handleExportJSON = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = `data:application/json;charset=utf-8,${encodeURIComponent(dataStr)}`;
    
    const link = document.createElement('a');
    link.setAttribute('href', dataUri);
    link.setAttribute('download', 'document-analysis.json');
    link.click();
  };

  const handleExportCSV = () => {
    let csvContent = 'Type,Text,Confidence,X1,Y1,X2,Y2\n';
    
    Object.entries(results.entities).forEach(([type, items]) => {
      items.forEach(item => {
        const { text, confidence, bbox } = item;
        const [x1, y1, x2, y2] = bbox;
        csvContent += `${type},"${text.replace(/"/g, '""')}",${confidence},${x1},${y1},${x2},${y2}\n`;
      });
    });
    
    const dataUri = `data:text/csv;charset=utf-8,${encodeURIComponent(csvContent)}`;
    const link = document.createElement('a');
    link.setAttribute('href', dataUri);
    link.setAttribute('download', 'document-analysis.csv');
    link.click();
  };

  const handleExportImage = () => {
    if (!documentImage) return;
    
    const link = document.createElement('a');
    link.href = documentImage;
    link.download = 'document-annotated.png';
    link.click();
  };

  return (
    <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
      <ButtonGroup variant="contained">
        <Button 
          startIcon={<FileDownloadIcon />} 
          onClick={handleExportJSON}
          color="primary"
        >
          JSON
        </Button>
        <Button 
          startIcon={<FileDownloadIcon />} 
          onClick={handleExportCSV}
          color="primary"
        >
          CSV
        </Button>
        <Button 
          startIcon={<FileDownloadIcon />} 
          onClick={handleExportImage}
          color="primary"
          disabled={!documentImage}
        >
          Annotated Image
        </Button>
      </ButtonGroup>
    </Box>
  );
};

export default ExportControls;