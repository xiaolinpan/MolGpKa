# Molecule Drawing Functionality Enhancement

## Overview

This update successfully integrates the pKa prediction functionality from `src/predict_pka.py` into `webserver/app.py` and adds molecule drawing capabilities that can generate highlighted molecular images for each predicted site.

## Main Features

### 1. pKa Prediction Integration

- **Core Functions**:
  - `load_model()`: Load trained models
  - `model_pred()`: Make predictions for specific atoms
  - `predict_acid()`: Predict pKa values for acidic sites
  - `predict_base()`: Predict pKa values for basic sites
  - `predict_pka_for_molecule()`: Main prediction function

- **Web API**:
  - `get_pka_predictions()`: Updated prediction API using real prediction models
  - Supports error handling and result formatting

### 2. Molecule Drawing Functionality

- **Core Function**:
  - `draw_mol_with_highlight()`: Draw molecules and highlight specified atoms

- **Features**:
  - Automatically remove hydrogen atoms for clearer images
  - Correctly map atom indices (indices change after removing H atoms)
  - Highlight corresponding heavy atoms
  - Support different displays for acidic and basic sites

### 3. Atom Mapping Algorithm

When removing hydrogen atoms, atom indices change. Our algorithm:

1. **Check Original Atom Type**:
   - If hydrogen atom: Find its connected heavy atom
   - If heavy atom: Calculate its new index in the H-free molecule

2. **Mapping Logic**:
   ```python
   # If original atom is hydrogen
   if original_atom.GetSymbol() == 'H':
       # Find connected heavy atom
       for bond in mol.GetBonds():
           if bond.GetBeginAtomIdx() == atom_idx:
               target_atom_idx = bond.GetEndAtomIdx()
               break
   
   # If original atom is heavy atom
   else:
       # Calculate new index
       heavy_count = 0
       for i in range(mol.GetNumAtoms()):
           if mol.GetAtomWithIdx(i).GetSymbol() != 'H':
               if i == atom_idx:
                   target_atom_idx = heavy_count
                   break
               heavy_count += 1
   ```

## File Structure

```
webserver/
├── app.py                           # Main application file (integrated prediction and drawing)
├── requirements.txt                  # Dependencies (updated)
├── templates/
│   └── index.html                   # Results page template (updated)
├── static/
│   ├── style.css                    # Stylesheet (updated)
│   └── molecule_images/             # Molecular image storage directory
├── test_integration.py              # Prediction functionality test script
├── test_molecule_drawing.py         # Molecule drawing test script
├── test_atom_mapping.py             # Atom mapping test script
├── INTEGRATION_README.md            # Integration documentation
└── MOLECULE_DRAWING_README.md       # This file
```

## Test Results

### Test Molecules

1. **Acetic Acid (CC(=O)O)**:
   - Original: 8 atoms (4 heavy atoms + 4 hydrogen atoms)
   - After H removal: 4 heavy atoms
   - Site 7 (hydrogen atom) → mapped to connected heavy atom

2. **Triethylamine (CCN(CC)CC)**:
   - Original: 22 atoms (7 heavy atoms + 15 hydrogen atoms)
   - After H removal: 7 heavy atoms
   - Site 2 (nitrogen atom) → correctly mapped

3. **Benzoic Acid (C1=CC=C(C=C1)C(=O)O)**:
   - Original: 15 atoms (9 heavy atoms + 6 hydrogen atoms)
   - After H removal: 9 heavy atoms
   - Site 9 (hydrogen atom) → mapped to connected heavy atom

### Generated Images

- Format: PNG
- Size: 300x300 pixels
- Features: No hydrogen atoms, highlighted corresponding heavy atoms
- Storage location: `static/molecule_images/`

## Web Interface Features

### 1. Molecule Display

- **Acidic Sites**: Red flame icon + highlighted display
- **Basic Sites**: Green leaf icon + highlighted display
- **Image Interaction**: Hover effects, click to zoom

### 2. pKa Value Display

- **Value Display**: Precise to 2 decimal places
- **Classification Labels**:
  - < 3: Strong Acid
  - 3-7: Weak Acid
  - 7-11: Weak Base
  - > 11: Strong Base

### 3. Responsive Design

- Mobile device support
- Adaptive image sizing
- Smooth animation effects

## Usage Instructions

### 1. Start Server

```bash
cd webserver
conda activate flask
python app.py --debug
```

### 2. Access Web Interface

- Address: `http://127.0.0.1:5000`
- Enter SMILES string
- View prediction results and molecular images

### 3. Test Functionality

```bash
# Test prediction functionality
python test_integration.py

# Test molecule drawing
python test_molecule_drawing.py

# Test atom mapping
python test_atom_mapping.py
```

## Technical Details

### Dependencies

- Flask==3.1.0
- rdkit==2025.03.5
- torch==2.7.1
- torch-scatter==2.1.1
- numpy, pandas

### Model Files

- `../models/weight_acid.pth` - Acidic site prediction model
- `../models/weight_base.pth` - Basic site prediction model

### Error Handling

- SMILES format validation
- Model loading error handling
- Image generation failure handling
- Atom mapping failure fallback mechanism

## Update Log

- **v1.0**: Initial integration with basic prediction functionality
- **v1.1**: Added molecule drawing functionality
- **v1.2**: Optimized atom mapping algorithm, removed H atom display
- **v1.3**: Enhanced web interface and styling

## Important Notes

1. **Performance Considerations**: Molecule drawing increases computation time
2. **Storage Space**: Image files consume disk space
3. **Concurrent Processing**: Recommend using image caching in production
4. **Atom Mapping**: Complex molecules may require more precise mapping algorithms 