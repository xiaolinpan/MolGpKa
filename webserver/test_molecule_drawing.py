#!/usr/bin/env python
# coding: utf-8

"""
Test script to verify the molecule drawing functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the prediction functions from app.py
from app import predict_pka_for_molecule, draw_mol_with_highlight

def test_prediction():
    """Test the pKa prediction functionality"""
    
    # Test SMILES strings
    test_smiles = [
        "CC(=O)O",  # Acetic acid
        "CCN(CC)CC",  # Triethylamine
        "C1=CC=C(C=C1)C(=O)O",  # Benzoic acid
    ]
    
    print("Testing molecule drawing functionality...")
    print("=" * 50)
    
    # Create static directory for images
    static_dir = os.path.join(os.path.dirname(__file__), 'static', 'molecule_images')
    os.makedirs(static_dir, exist_ok=True)
    
    for i, smiles in enumerate(test_smiles, 1):
        print(f"\nTest {i}: {smiles}")
        print("-" * 30)
        
        try:
            base_dict, acid_dict, mol, error = predict_pka_for_molecule(smiles)
            
            if error:
                print(f"Error: {error}")
            else:
                print("Acid predictions:")
                for site_id, pka in acid_dict.items():
                    print(f"  Site {site_id}: pKa = {pka:.2f}")
                    # Draw molecule with highlight
                    image_filename = f"test_acid_site_{site_id}_{i}.png"
                    image_path = os.path.join(static_dir, image_filename)
                    success = draw_mol_with_highlight(mol, site_id, image_path)
                    print(f"    Image saved: {image_path} (Success: {success})")
                
                print("Base predictions:")
                for site_id, pka in base_dict.items():
                    print(f"  Site {site_id}: pKa = {pka:.2f}")
                    # Draw molecule with highlight
                    image_filename = f"test_base_site_{site_id}_{i}.png"
                    image_path = os.path.join(static_dir, image_filename)
                    success = draw_mol_with_highlight(mol, site_id, image_path)
                    print(f"    Image saved: {image_path} (Success: {success})")
                
                if not acid_dict and not base_dict:
                    print("No ionizable sites found")
                    
        except Exception as e:
            print(f"Exception occurred: {e}")
    
    print("\n" + "=" * 50)
    print("Molecule drawing test completed!")
    print(f"Images saved in: {static_dir}")

if __name__ == "__main__":
    test_prediction() 