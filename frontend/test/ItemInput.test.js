
// a. ItemInput Component:
// Test rendering: Ensure the component renders without crashing and displays the correct input fields.
// Test input change: Simulate user typing in the input fields and ensure the state updates correctly.
// Test zip code input: Ensure that the zip code input accepts valid entries and handles invalid entries appropriately.
import { fireEvent, render, screen  } from '@testing-library/react';
import ItemInput from '../src/ItemInput';
import React from 'react';
import App from '../src/App';
import '@testing-library/jest-dom/extend-expect';



describe('ItemInput Component', () => {
    
    // Test rendering
    it('renders without crashing and displays the correct input fields', () => {
        render(<ItemInput />);
        
        // Using screen to query the DOM by label text
        expect(screen.getByLabelText('Add Item')).toBeInTheDocument();
        expect(screen.getByLabelText('Zip Code')).toBeInTheDocument();
    });

    // Test input change for item name
    it('updates the item name when typed into the item input field', () => {
        const handleItemChange = jest.fn();
        render(<ItemInput onItemChange={handleItemChange} />);

        const itemInput = screen.getByLabelText('Add Item');
        fireEvent.change(itemInput, { target: { value: 'Milk' } });

        expect(handleItemChange).toHaveBeenCalledWith('Milk');
    });

    // Test input change for zip code
    it('updates the zip code when typed into the zip code input field', () => {
        const handleZipChange = jest.fn();
        render(<ItemInput onZipChange={handleZipChange} />);

        const zipInput = screen.getByLabelText('Zip Code');
        fireEvent.change(zipInput, { target: { value: '12345' } });

        expect(handleZipChange).toHaveBeenCalledWith('12345');
    });

    // Test invalid zip code entry
    // This test assumes some form of validation is implemented in the ItemInput component
    it('handles invalid zip code entries appropriately', () => {
        const handleZipChange = jest.fn();
        render(<ItemInput onZipChange={handleZipChange} />);

        const zipInput = screen.getByLabelText('Zip Code');
        fireEvent.change(zipInput, { target: { value: '1234a' } });

        // Assuming there's a validation message displayed for invalid zip codes
        expect(screen.getByText('Invalid zip code')).toBeInTheDocument();
    });
});
