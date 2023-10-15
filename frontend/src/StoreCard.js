import React from 'react';
import { Card, CardContent, Typography, Divider } from '@mui/material';

const StoreCard = ({ storeName, items, totalPrice, isCheapest, totalItems, loading }) => {
    return (
        <Card variant="outlined" sx={{ borderColor: isCheapest ? 'green' : 'grey.300', width: 500, height: 250, borderRadius: 5}}>
            <CardContent>
                <Typography variant="h6" component="div" color={isCheapest ? 'green' : 'text.primary'}>
                    {storeName}
                </Typography>
                <Typography variant={isCheapest ? 'h5' : 'h6'} component="p" fontWeight={isCheapest ? 'bold' : 'normal'} color={isCheapest ? 'green' : 'text.primary'}>
                    Total: ${totalPrice.toFixed(2)}
                </Typography>
                < Divider 
            style={{
              margin:".5rem",
            }}/>
                {items.map(item => (
                    <Typography key={item.name} variant="body1" component="p" background="green">
                        ${item.price.toFixed(2)} - {item.name}
                    </Typography>
                ))}
                {items.length < totalItems && loading === "idle" && 
    <Typography variant="body2" component="p" color="error">
        Some items could not be found at this store.
    </Typography>
}
            </CardContent>
        </Card>
    );
};

export default StoreCard;
