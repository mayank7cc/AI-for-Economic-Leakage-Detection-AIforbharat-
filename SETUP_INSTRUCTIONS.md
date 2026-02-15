# Setup Instructions

## Fix Missing Dependencies

You need to install the required packages. Here are your options:

### Option 1: Use Existing Virtual Environment (Recommended)

```bash
# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Create New Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Install Globally (Not Recommended)

```bash
pip install -r requirements.txt
```

## Verify Installation

After installing, verify with:

```bash
python -c "from models import AnomalyDetector; print('Success!')"
```

## Run the Pipeline

Once dependencies are installed:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Run the complete pipeline
python pipeline.py

# Or run individual steps
python notebooks/preprocess.py
python notebooks/detect_anomalies.py
python notebooks/calculate_risk.py

# Start the API server
python backend/app.py
```

## Common Issues

### Issue: ModuleNotFoundError
**Solution**: Make sure you've activated the virtual environment and installed requirements.txt

### Issue: File not found errors
**Solution**: Make sure you've run the data generator first:
```bash
python notebooks/data_generator.py
```

### Issue: Import errors
**Solution**: Make sure you're running commands from the project root directory
