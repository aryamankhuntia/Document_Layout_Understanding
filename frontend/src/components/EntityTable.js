import React, { useState } from 'react'; // Added useState import
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper, 
  Chip,
  Box // Added Box import
} from '@mui/material';

const EntityTable = ({ entities }) => {
  const entityTypes = Object.keys(entities);
  const [expandedType, setExpandedType] = useState(entityTypes[0]);

  const handleTypeClick = (type) => {
    setExpandedType(expandedType === type ? null : type);
  };

  return (
    <TableContainer component={Paper} variant="outlined">
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Entity Type</TableCell>
            <TableCell>Count</TableCell>
            <TableCell>Preview</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {entityTypes.map((type) => (
            <React.Fragment key={type}>
              <TableRow 
                hover 
                onClick={() => handleTypeClick(type)}
                sx={{ cursor: 'pointer', backgroundColor: expandedType === type ? '#f0f7ff' : 'inherit' }}
              >
                <TableCell>
                  <Chip 
                    label={type} 
                    color={
                      type === 'header' ? 'primary' : 
                      type === 'question' ? 'secondary' : 
                      'default'
                    } 
                  />
                </TableCell>
                <TableCell>{entities[type].length}</TableCell>
                <TableCell>
                  {entities[type].slice(0, 3).map((entity, idx) => (
                    <span key={idx} style={{ marginRight: '8px' }}>
                      {entity.text.length > 20 
                        ? `${entity.text.substring(0, 20)}...` 
                        : entity.text}
                    </span>
                  ))}
                </TableCell>
              </TableRow>
              
              {expandedType === type && entities[type].map((entity, index) => (
                <TableRow key={index}>
                  <TableCell colSpan={3}>
                    <Box sx={{ pl: 4, display: 'flex', justifyContent: 'space-between' }}>
                      <div>
                        <strong>Text:</strong> {entity.text}
                      </div>
                      <div>
                        <strong>Confidence:</strong> {(entity.confidence * 100).toFixed(1)}%
                      </div>
                      <div>
                        <strong>Position:</strong> {entity.bbox.join(', ')}
                      </div>
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </React.Fragment>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default EntityTable;