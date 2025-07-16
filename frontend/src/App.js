import React, { useState } from 'react';
import DocumentUpload from './components/DocumentUpload';
import ResultsDisplay from './components/ResultsDisplay';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme();

function App() {
  const [results, setResults] = useState(null);
  const [documentImage, setDocumentImage] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleUpload = async (file) => {
    setProcessing(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Create a preview URL for the image
      setDocumentImage(URL.createObjectURL(file));
      
      const response = await fetch('http://localhost:8000/document/parse', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Document processing failed');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Error processing document: ' + err.message);
      console.error(err);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>
          Document Layout Understanding
        </h1>
        
        <DocumentUpload onUpload={handleUpload} disabled={processing} />
        
        {processing && (
          <div style={{ textAlign: 'center', margin: '20px 0' }}>
            <p>Processing document...</p>
            <div className="spinner"></div>
          </div>
        )}
        
        {error && (
          <div style={{ color: 'red', textAlign: 'center', margin: '10px 0' }}>
            {error}
          </div>
        )}
        
        {results && (
          <ResultsDisplay results={results} documentImage={documentImage} />
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;