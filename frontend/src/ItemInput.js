import React, { useState } from 'react';
import { TextField } from '@mui/material';
import axios from 'axios';

const ItemInput = ({ currentItem, onItemChange, onAddItem }) => {

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
        </div>
    );
};


export default ItemInput;
