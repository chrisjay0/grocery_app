import React from 'react';
import { TextField } from '@mui/material';

const ItemInput = ({ currentItem, onItemChange, onAddItem, currentZip, onZipChange }) => {
    const handleAddItem = async () => {
        if (currentItem.trim()) {
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
                onChange={e => onZipChange(e.target.value)}
                fullWidth
                style={{ marginTop: '10px' }} // Add some margin for spacing
            />
        </div>
    );
};

export default ItemInput;
