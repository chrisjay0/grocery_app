#!/bin/sh

# Navigate to frontend and build the React app
cd frontend && npm install && npm run build

# Navigate to backend and install Python dependencies
cd ../backend && pip install -r requirements.txt
