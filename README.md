# AI-Assisted Box Selection System

A lightweight Django REST service for ecommerce warehouse box optimization. Evaluates item dimensions, weights, and quantities to recommend the lowest-cost shipping container.

## Features
- **3D Spatial Rotation Check**: Automatically determines if an item fits by evaluating sorted dimensional bounds.
- **Cost Minimization**: Sorts eligible containers by cost to pick the most economical box.
- **Automated Tests**: Unit and integration test coverage for capacity thresholds and API responses.

## Setup & Running Locally

1. **Activate Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt