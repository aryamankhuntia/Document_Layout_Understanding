import React, { useRef, useEffect } from 'react';
import { Box, Typography } from '@mui/material';

const VisualizationPane = ({ entities, documentImage }) => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    if (!documentImage || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      // Set canvas dimensions to match image
      canvas.width = img.width;
      canvas.height = img.height;
      
      // Draw image
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      
      // Draw bounding boxes
      Object.entries(entities).forEach(([type, items]) => {
        items.forEach(item => {
          const [x1, y1, x2, y2] = item.bbox;
          
          // Choose color based on entity type
          let color;
          switch(type) {
            case 'header': color = 'rgba(25, 118, 210, 0.5)'; break;
            case 'question': color = 'rgba(220, 0, 78, 0.5)'; break;
            case 'answer': color = 'rgba(56, 142, 60, 0.5)'; break;
            default: color = 'rgba(158, 158, 158, 0.5)';
          }
          
          // Draw bounding box
          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
          
          // Draw label background
          ctx.fillStyle = color;
          ctx.fillRect(x1, y1 - 20, 80, 20);
          
          // Draw label text
          ctx.fillStyle = 'white';
          ctx.font = '12px Arial';
          ctx.fillText(type, x1 + 5, y1 - 5);
        });
      });
    };
    
    img.src = documentImage;
  }, [documentImage, entities]);

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        Document with layout annotations (color-coded by entity type)
      </Typography>
      <Box sx={{ overflow: 'auto', maxHeight: '70vh', border: '1px solid #ddd' }}>
        <canvas ref={canvasRef} style={{ display: 'block' }} />
      </Box>
    </Box>
  );
};

export default VisualizationPane;