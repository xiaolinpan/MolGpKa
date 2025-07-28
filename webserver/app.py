from flask import Flask, render_template, request
import os
import json
import sys

# Add the src directory to the path to import utils modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import pKa prediction modules
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import Draw

import numpy as np
import pandas as pd
import torch
from utils.ionization_group import get_ionization_aid
from utils.descriptor import mol2vec
from utils.net import GCNNet


app = Flask(__name__)

# Counter functionality
COUNTER_FILE = 'visitor_counter.json'

def load_counter():
    """Load visitor counter from file"""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
                count = data.get('total_visitors', 0)
                print(f"Loaded counter from file: {count}")
                return count
        except Exception as e:
            print(f"Error loading counter: {e}")
            return 0
    print("Counter file doesn't exist, starting from 0")
    return 0

def save_counter(count):
    """Save visitor counter to file"""
    try:
        with open(COUNTER_FILE, 'w') as f:
            json.dump({'total_visitors': count}, f)
        print(f"Saved counter to file: {count}")
    except Exception as e:
        print(f"Error saving counter: {e}")

def increment_counter():
    """Increment and save visitor counter"""
    count = load_counter() + 1
    save_counter(count)
    print(f"Counter incremented to: {count}")
    return count

# pKa prediction functions integrated from predict_pka.py
def load_model(model_file, device="cpu"):
    """Load the trained model"""
    model = GCNNet().to(device)
    model.load_state_dict(torch.load(model_file, map_location=device))
    model.eval()
    return model

def model_pred(m2, aid, model, device="cpu"):
    """Make prediction for a specific atom index"""
    data = mol2vec(m2, aid)
    with torch.no_grad():
        data = data.to(device)
        pKa = model(data)
        pKa = pKa.cpu().numpy()
        pka = pKa[0][0]
    return pka

def predict_acid(mol):
    """Predict pKa values for acidic sites"""
    model_file = os.path.join(os.path.dirname(__file__), '..', 'models', 'weight_acid.pth')
    model_acid = load_model(model_file)

    acid_idxs = get_ionization_aid(mol, acid_or_base="acid")
    acid_res = {}
    for aid in acid_idxs:
        apka = model_pred(mol, aid, model_acid)
        acid_res.update({aid: apka})
    return acid_res

def draw_mol_with_highlight(mol, atom_idx, image_path):
    """Draw the molecule with the atom index highlighted (without H atoms)"""
    try:
        # Create a copy of the molecule without hydrogens for display
        mol_no_h = Chem.RemoveHs(mol)
        
        # Get the atom that corresponds to the original atom_idx in the molecule with H
        # We need to find the heavy atom that the original atom_idx points to
        original_atom = mol.GetAtomWithIdx(atom_idx)
        
        # Find the corresponding atom in the molecule without H
        # This is tricky because removing H atoms changes the atom indices
        # We'll use atom properties or coordinates to match atoms
        
        # Method 1: Use atom properties to find the corresponding heavy atom
        target_atom_idx = None
        
        # If the original atom is a hydrogen, find its parent heavy atom
        if original_atom.GetSymbol() == 'H':
            # Find the heavy atom this hydrogen is bonded to
            for bond in mol.GetBonds():
                if bond.GetBeginAtomIdx() == atom_idx:
                    target_atom_idx = bond.GetEndAtomIdx()
                    break
                elif bond.GetEndAtomIdx() == atom_idx:
                    target_atom_idx = bond.GetBeginAtomIdx()
                    break
        else:
            # If it's already a heavy atom, we need to find its new index in mol_no_h
            # We'll use a simple approach: count heavy atoms up to this point
            heavy_count = 0
            for i in range(mol.GetNumAtoms()):
                if mol.GetAtomWithIdx(i).GetSymbol() != 'H':
                    if i == atom_idx:
                        target_atom_idx = heavy_count
                        break
                    heavy_count += 1
        
        # If we couldn't find the target atom, use the original index (fallback)
        if target_atom_idx is None:
            target_atom_idx = atom_idx
        
        # Create a drawer
        drawer = Draw.MolDraw2DCairo(300, 300)
        
        # Create highlight info for the heavy atom
        highlight_atoms = [target_atom_idx]
        highlight_radii = {target_atom_idx: 0.5}  # Highlight radius for the center atom
        
        # Draw the molecule without H atoms, with highlights
        drawer.DrawMolecule(mol_no_h, highlightAtoms=highlight_atoms, highlightAtomRadii=highlight_radii)
        drawer.FinishDrawing()
        
        # Save the image
        drawer.WriteDrawingText(image_path)
        
        return True
    except Exception as e:
        print(f"Error drawing molecule: {e}")
        return False

def predict_base(mol):
    """Predict pKa values for basic sites"""
    model_file = os.path.join(os.path.dirname(__file__), '..', 'models', 'weight_base.pth')
    model_base = load_model(model_file)

    base_idxs = get_ionization_aid(mol, acid_or_base="base")
    base_res = {}
    for aid in base_idxs:
        bpka = model_pred(mol, aid, model_base) 
        base_res.update({aid: bpka})
    return base_res


def predict_pka_for_molecule(smiles, uncharged=True):
    """Main prediction function for a given SMILES string"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None, None, "Invalid SMILES string"
        
        if uncharged:
            un = rdMolStandardize.Uncharger()
            mol = un.uncharge(mol)
            mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
        
        mol = AllChem.AddHs(mol)
        base_dict = predict_base(mol)
        acid_dict = predict_acid(mol)
        
        return base_dict, acid_dict, mol, None
    except Exception as e:
        return None, None, None, f"Error in prediction: {str(e)}"

# Updated pKa prediction API
def get_pka_predictions(smiles=None):
    """
    Get pKa predictions for a given SMILES string.
    Returns a list of prediction dictionaries with site information and pKa values.
    """
    predictions = []
    
    if smiles and smiles.strip():
        print(f"Received SMILES: {smiles}")
        
        # Use the real prediction function
        base_dict, acid_dict, mol, error = predict_pka_for_molecule(smiles)
        
        if error:
            print(f"Prediction error: {error}")
            # Return mock data if prediction fails
            for i in range(1, 6):
                predictions.append({
                    'site_type': 'error',
                    'site_id': i,
                    'pka_value': 0.0,
                    'error_message': error,
                    'image_path': None
                })
        else:
            # Create static directory for images if it doesn't exist
            static_dir = os.path.join(os.path.dirname(__file__), 'static', 'molecule_images')
            os.makedirs(static_dir, exist_ok=True)
            
            # Process acid predictions
            for site_id, pka_value in acid_dict.items():
                # Generate image path
                image_filename = f"acid_site_{site_id}_{hash(smiles)}.png"
                image_path = os.path.join(static_dir, image_filename)
                web_path = f"/static/molecule_images/{image_filename}"
                
                # Draw molecule with highlight
                if mol is not None:
                    draw_mol_with_highlight(mol, site_id, image_path)
                
                predictions.append({
                    'site_type': 'acid',
                    'site_id': site_id,
                    'pka_value': round(pka_value, 2),
                    'image_path': web_path
                })
            
            # Process base predictions
            for site_id, pka_value in base_dict.items():
                # Generate image path
                image_filename = f"base_site_{site_id}_{hash(smiles)}.png"
                image_path = os.path.join(static_dir, image_filename)
                web_path = f"/static/molecule_images/{image_filename}"
                
                # Draw molecule with highlight
                if mol is not None:
                    draw_mol_with_highlight(mol, site_id, image_path)
                
                predictions.append({
                    'site_type': 'base',
                    'site_id': site_id,
                    'pka_value': round(pka_value, 2),
                    'image_path': web_path
                })
            
            # If no predictions found, add a placeholder
            if not predictions:
                predictions.append({
                    'site_type': 'no_sites',
                    'site_id': 1,
                    'pka_value': 0.0,
                    'message': 'No ionizable sites found',
                    'image_path': None
                })
    else:
        # Default demo data when no SMILES is provided
        for i in range(1, 26):
            predictions.append({
                'site_type': 'demo',
                'site_id': i,
                'pka_value': round(7.0 + (i * 0.1), 2),
                'image_path': f"https://via.placeholder.com/300x200?text=Demo+Site+{i}"
            })
    
    return predictions

@app.route('/')
def home():
    visitor_count = increment_counter()
    return render_template('input.html', visitor_count=visitor_count)

@app.route('/results')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '', type=str)
    smiles = request.args.get('smiles', '', type=str)
    
    # Debug: print received SMILES
    if smiles:
        print(f"Received SMILES from form: {smiles}")
    
    all_predictions = get_pka_predictions(smiles)
    
    # Filter predictions based on search query
    if search_query:
        all_predictions = [pred for pred in all_predictions if search_query.lower() in str(pred.get('site_type', '')).lower()]
    
    total_predictions = len(all_predictions)
    start = (page - 1) * per_page
    end = start + per_page
    predictions_on_page = all_predictions[start:end]
    
    total_pages = (total_predictions + per_page - 1) // per_page
    
    return render_template('index.html', 
                           predictions=predictions_on_page,
                           page=page,
                           total_pages=total_pages,
                           search_query=search_query,
                           visitor_count=load_counter(),
                           smiles_input=smiles)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='MolGpKa Web Server')
    parser.add_argument('--port', '-p', type=int, default=int(os.environ.get('PORT', 5000)),
                        help='Port to run the server on (default: 5000)')
    parser.add_argument('--host', '-H', default=os.environ.get('HOST', '127.0.0.1'),
                        help='Host to run the server on (default: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true', default=True,
                        help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"Starting MolGpKa server on {args.host}:{args.port}")
    app.run(debug=args.debug, port=args.port, host=args.host)
