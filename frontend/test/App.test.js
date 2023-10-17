

import React from 'react';
import { render, screen, fireEvent  } from '@testing-library/react';
import App from '../src/App';
import '@testing-library/jest-dom/extend-expect';


test('Grocery Price Comparator', () => {
  render(<App />);
  const linkElement = screen.getByText(/Grocery Price Comparator/i);
  expect(linkElement).toBeInTheDocument();
});

test('renders main components', () => {
  render(<App />);
  const inputElement = screen.getByLabelText(/Add Item/i);
  const zipInputElement = screen.getByLabelText(/Zip Code/i);
  const addButton = screen.getByLabelText(/Add Item/i);
  expect(inputElement).toBeInTheDocument();
  expect(zipInputElement).toBeInTheDocument();
  expect(addButton).toBeInTheDocument();
});

test('adds an item to the list', () => {
  render(<App />);
  
  const inputElement = screen.getByRole('textbox', { name: /Add Item/i });
  
  const addButton = screen.getByRole('button', { name: /Add Item/i });

  fireEvent.change(inputElement, { target: { value: 'Milk' } });
  fireEvent.click(addButton);

  const listItem = screen.getByText(/Milk/i);
  expect(listItem).toBeInTheDocument();
});
