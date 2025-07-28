#!/usr/bin/env python
# coding: utf-8

"""
Test script to verify the integration of pKa prediction functions into app.py
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the prediction functions from app.py
from app import predict_pka_for_molecule

def test_prediction():
    """Test the pKa prediction functionality"""
    
    # Test SMILES strings (corrected formats)
    test_smiles = [
        "CC(=O)O",  # Acetic acid (corrected)
        "CCN(CC)CC",  # Triethylamine
        "C1=CC=C(C=C1)C(=O)O",  # Benzoic acid
        "CN(C)C",  # Dimethylamine
    ]
    
    print("Testing pKa prediction integration...")
    print("=" * 50)
    
    for i, smiles in enumerate(test_smiles, 1):
        print(f"\nTest {i}: {smiles}")
        print("-" * 30)
        
        try:
            base_dict, acid_dict, error = predict_pka_for_molecule(smiles)
            
            if error:
                print(f"Error: {error}")
            else:
                print("Acid predictions:")
                for site_id, pka in acid_dict.items():
                    print(f"  Site {site_id}: pKa = {pka:.2f}")
                
                print("Base predictions:")
                for site_id, pka in base_dict.items():
                    print(f"  Site {site_id}: pKa = {pka:.2f}")
                
                if not acid_dict and not base_dict:
                    print("No ionizable sites found")
                    
        except Exception as e:
            print(f"Exception occurred: {e}")
    
    print("\n" + "=" * 50)
    print("Integration test completed!")

if __name__ == "__main__":
    test_prediction() 