import React, { useState } from 'react';
import { Tabs, Tab, Box, Paper, Typography } from '@mui/material';
import EntityTable from './EntityTable';
import VisualizationPane from './VisualizationPane';
import ExportControls from './ExportControls';

const ResultsDisplay = ({ results, documentImage }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Analysis Results
      </Typography>
      
      <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Structured Data" />
        <Tab label="Visualization" />
        <Tab label="Raw JSON" />
      </Tabs>
      
      <Box>
        {activeTab === 0 && (
          <EntityTable entities={results.entities} />
        )}
        
        {activeTab === 1 && (
          <VisualizationPane 
            entities={results.entities} 
            documentImage={documentImage} 
          />
        )}
        
        {activeTab === 2 && (
          <Box sx={{ 
            backgroundColor: '#f5f5f5', 
            p: 2, 
            borderRadius: 1,
            maxHeight: '500px',
            overflow: 'auto'
          }}>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </Box>
        )}
      </Box>
      
      <ExportControls results={results} documentImage={documentImage} />
    </Paper>
  );
};

export default ResultsDisplay;