# MolGpKa Web Server

A Flask-based web application for pKa prediction with molecular visualization.

## Features

- **Interactive Molecular Drawing**: Draw molecules using JSME molecular editor
- **pKa Prediction**: Predict pKa values for acidic and basic sites in molecules
- **Molecular Visualization**: Generate images with highlighted ionization sites
- **Responsive Design**: Modern, mobile-friendly web interface
- **Real-time Results**: Instant pKa predictions with visual feedback

## Quick Start

### Prerequisites

1. **Conda Environment**: Make sure you have the `flask` conda environment activated
   ```bash
   conda activate flask
   ```

2. **Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

### Starting the Server

1. **Navigate to webserver directory**:
   ```bash
   cd MolGpKa/webserver
   ```

2. **Start the Flask application**:
   ```bash
   python app.py
   ```

3. **Access the web interface**:
   - Open your browser and go to: `http://127.0.0.1:5000`
   - The server will start on localhost port 5000

### Usage

1. **Input Methods**:
   - **SMILES Input**: Enter SMILES string directly in the text field
   - **Molecular Drawing**: Use the JSME editor to draw molecules interactively

2. **Prediction Process**:
   - Enter or draw your molecule
   - Click "Predict pKa Values"
   - View results with molecular images and pKa values

3. **Results Display**:
   - **Molecular Images**: Each ionization site is highlighted
   - **pKa Values**: Numerical predictions for each site
   - **Statistics**: Summary of acidic and basic sites
   - **Pagination**: Results split across multiple pages

## File Structure

```
webserver/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── visitor_counter.json     # Visitor tracking
├── static/                  # Static assets
│   ├── style.css           # CSS styles
│   ├── molecule_images/    # Generated molecule images
│   ├── images/             # Static images
│   └── js/                 # JavaScript files
└── templates/              # HTML templates
    ├── index.html         # Results page
    └── input.html         # Input page
```

## Technical Details

### Core Components

- **pKa Prediction**: Integrated with MolGpKa prediction models
- **Molecular Drawing**: JSME molecular editor integration
- **Image Generation**: RDKit-based molecular visualization
- **Web Framework**: Flask with Bootstrap styling

### Key Features

- **Atom Mapping**: Correctly highlights heavy atoms after H removal
- **Site Classification**: Distinguishes between acidic and basic sites
- **Responsive Layout**: Optimized for desktop and mobile devices
- **Error Handling**: Graceful handling of invalid inputs

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you're in the `flask` conda environment
2. **Port already in use**: Change port or kill existing process
3. **Model loading errors**: Check that model files exist in `../models/`

### Debug Mode

To run with debug information:
```bash
python app.py --debug
```

## Development

The web server integrates the pKa prediction functionality from `src/predict_pka.py` and provides a user-friendly web interface for molecular pKa prediction with visual results.