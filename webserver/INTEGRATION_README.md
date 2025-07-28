# MolGpKa Web Server Integration

## Overview

This project has successfully integrated the pKa prediction functionality from `src/predict_pka.py` into `webserver/app.py`. The web server can now use real pKa prediction models directly.

## Integrated Features

### 1. Core Prediction Functions

- `load_model()`: Load trained models
- `model_pred()`: Make predictions for specific atoms
- `predict_acid()`: Predict pKa values for acidic sites
- `predict_base()`: Predict pKa values for basic sites
- `predict_pka_for_molecule()`: Main prediction function for SMILES strings

### 2. Updated Web API

- `get_pka_predictions()`: Updated prediction API that now uses real prediction models
- Supports error handling and result formatting

## File Structure

```
webserver/
├── app.py                    # Main application file (integrated prediction functionality)
├── requirements.txt          # Dependencies (updated)
├── templates/
│   └── index.html           # Results page template (updated)
├── test_integration.py      # Test script
└── INTEGRATION_README.md    # This file
```

## Installation and Setup

### 1. Install Dependencies

```bash
cd webserver
pip install -r requirements.txt
```

### 2. Run Server

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`.

### 3. Test Integration

```bash
python test_integration.py
```

## Usage

### Web Interface

1. Visit `http://127.0.0.1:5000`
2. Enter SMILES string in the input box
3. Click submit button
4. View prediction results

### API Calls

```python
from app import predict_pka_for_molecule

# Predict single molecule
smiles = "CC(=O)O"  # Acetic acid
base_dict, acid_dict, error = predict_pka_for_molecule(smiles)

if error:
    print(f"Error: {error}")
else:
    print("Acid predictions:", acid_dict)
    print("Base predictions:", base_dict)
```

## Prediction Result Format

### Successful Prediction

```python
{
    'site_type': 'acid',      # 'acid' or 'base'
    'site_id': 1,             # Site ID
    'pka_value': 4.76         # pKa value
}
```

### Error Case

```python
{
    'site_type': 'error',
    'site_id': 1,
    'pka_value': 0.0,
    'error_message': 'Error message'
}
```

## Dependencies

- Flask==2.0.1
- Werkzeug==2.0.3
- rdkit-pypi
- torch
- numpy
- pandas

## Model Files

Ensure the following model files exist in the correct location:

- `../models/weight_acid.pth` - Acidic site prediction model
- `../models/weight_base.pth` - Basic site prediction model

## Important Notes

1. **Path Setup**: Code automatically adds the `src` directory to Python path
2. **Model Loading**: Model file paths use relative paths, ensure running from webserver directory
3. **Error Handling**: Includes complete error handling mechanism
4. **Memory Usage**: Model loading consumes memory, recommend using model caching in production

## Troubleshooting

### Common Issues

1. **Module Import Error**
   - Ensure running from webserver directory
   - Check if src directory exists

2. **Model File Not Found**
   - Confirm model file paths are correct
   - Check file permissions

3. **Dependency Installation Failure**
   - Use conda environment (recommended)
   - Check Python version compatibility

### Debug Mode

Start server with debug mode:

```bash
python app.py --debug
```

## Update Log

- **v1.0**: Initial integration with basic prediction functionality
- Support SMILES input and pKa prediction
- Complete error handling mechanism
- Updated web interface display 