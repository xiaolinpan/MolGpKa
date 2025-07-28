#!/usr/bin/env python
# coding: utf-8

"""
Test script to verify atom mapping and molecule drawing functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the prediction functions from app.py
from app import predict_pka_for_molecule, draw_mol_with_highlight
from rdkit import Chem
from rdkit.Chem import AllChem

def test_atom_mapping():
    """Test atom mapping between molecules with and without H atoms"""
    
    # Test SMILES strings
    test_smiles = [
        "CC(=O)O",  # Acetic acid
        "CCN(CC)CC",  # Triethylamine
        "C1=CC=C(C=C1)C(=O)O",  # Benzoic acid
    ]
    
    print("Testing atom mapping and molecule drawing...")
    print("=" * 60)
    
    # Create static directory for images
    static_dir = os.path.join(os.path.dirname(__file__), 'static', 'molecule_images')
    os.makedirs(static_dir, exist_ok=True)
    
    for i, smiles in enumerate(test_smiles, 1):
        print(f"\nTest {i}: {smiles}")
        print("-" * 40)
        
        try:
            base_dict, acid_dict, mol, error = predict_pka_for_molecule(smiles)
            
            if error:
                print(f"Error: {error}")
                continue
                
            # Create molecule without H atoms for comparison
            mol_no_h = Chem.RemoveHs(mol)
            
            print(f"Original molecule (with H): {mol.GetNumAtoms()} atoms")
            print(f"Molecule without H: {mol_no_h.GetNumAtoms()} atoms")
            
            # Print atom information for original molecule
            print("\nOriginal molecule atoms:")
            for idx in range(mol.GetNumAtoms()):
                atom = mol.GetAtomWithIdx(idx)
                print(f"  Atom {idx}: {atom.GetSymbol()}")
            
            # Print atom information for molecule without H
            print("\nMolecule without H atoms:")
            for idx in range(mol_no_h.GetNumAtoms()):
                atom = mol_no_h.GetAtomWithIdx(idx)
                print(f"  Atom {idx}: {atom.GetSymbol()}")
            
            print("\nAcid predictions:")
            for site_id, pka in acid_dict.items():
                print(f"  Site {site_id}: pKa = {pka:.2f}")
                # Draw molecule with highlight
                image_filename = f"test_acid_site_{site_id}_{i}_no_h.png"
                image_path = os.path.join(static_dir, image_filename)
                success = draw_mol_with_highlight(mol, site_id, image_path)
                print(f"    Image saved: {image_path} (Success: {success})")
            
            print("\nBase predictions:")
            for site_id, pka in base_dict.items():
                print(f"  Site {site_id}: pKa = {pka:.2f}")
                # Draw molecule with highlight
                image_filename = f"test_base_site_{site_id}_{i}_no_h.png"
                image_path = os.path.join(static_dir, image_filename)
                success = draw_mol_with_highlight(mol, site_id, image_path)
                print(f"    Image saved: {image_path} (Success: {success})")
            
            if not acid_dict and not base_dict:
                print("No ionizable sites found")
                    
        except Exception as e:
            print(f"Exception occurred: {e}")
    
    print("\n" + "=" * 60)
    print("Atom mapping test completed!")
    print(f"Images saved in: {static_dir}")

if __name__ == "__main__":
    test_atom_mapping() 