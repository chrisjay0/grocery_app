import React, { useState } from 'react';
import { TextField } from '@mui/material';

const ItemInput = ({ currentItem, onItemChange, onAddItem, currentZip, onZipChange, showComparison }) => {
    const [zipError, setZipError] = useState('');

    const validateZip = (zip) => {
        // Basic validation for a 5-digit zip code
        if (!/^\d{5}$/.test(zip)) {
            setZipError('Invalid zip code');
            return false;
        }
        setZipError(''); // Clear error if zip is valid
        return true;
    };

    const handleZipInputChange = (e) => {
        const zip = e.target.value;
        onZipChange(zip); // Update the zip code
        validateZip(zip); // Validate the new zip code
    };

    const handleAddItem = async () => {
        if (currentItem.trim() && validateZip(currentZip)) {
            onAddItem(currentItem);
        }
    };

    return (
        <div>
            <TextField 
                label="Add Item" 
                variant="outlined" 
                value={currentItem}
                onChange={e => onItemChange(e.target.value)}
                fullWidth
                style={{ borderRadius: 'px' }} 
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        handleAddItem();
                    }
                }}
            />
            <TextField 
                label="Zip Code" 
                variant="outlined" 
                value={currentZip}
                onChange={handleZipInputChange}
                fullWidth
                disabled={showComparison}
                style={{ marginTop: '10px' }} // Add some margin for spacing
                error={Boolean(zipError)}
                helperText={zipError}
            />
        </div>
    );
};

export default ItemInput;
