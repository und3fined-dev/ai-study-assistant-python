#!/bin/bash

# Start FastAPI backend in background using absolute path
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be ready
sleep 3

# Start Streamlit frontend
cd /app/frontend && streamlit run app.py --server.port 7860 --server.address 0.0.0.0
