import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const StoreCard = ({ storeName, items, totalPrice, isCheapest }) => {
    return (
        <Card variant="outlined" sx={{ borderColor: isCheapest ? 'green' : 'grey.300', width: 500, height: 250  }}>
            <CardContent>
                <Typography variant="h6" component="div" color={isCheapest ? 'green' : 'text.primary'}>
                    {storeName}
                </Typography>
                <Typography variant={isCheapest ? 'h5' : 'h6'} component="p" fontWeight={isCheapest ? 'bold' : 'normal'} color={isCheapest ? 'green' : 'text.primary'}>
                    Total: ${totalPrice.toFixed(2)}
                </Typography>
                {items.map(item => (
                    <Typography key={item.name} variant="body2" component="p">
                        ${item.price.toFixed(2)} - {item.name}
                    </Typography>
                ))}
            </CardContent>
        </Card>
    );
};

export default StoreCard;
