"""
Batch processing example for multiple SMILES strings.

This script demonstrates how to process multiple molecules efficiently
using the SMILEStoImage library.
"""

import os
from smiles_to_image import smiles_to_file

# List of common molecules with SMILES and identifiers
molecules = [
    ("CCO", "ethanol"),
    ("c1ccccc1", "benzene"),
    ("CC(=O)O", "acetic_acid"),
    ("CC(C)O", "isopropanol"),
    ("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "caffeine"),
    ("CC(=O)Oc1ccccc1C(=O)O", "aspirin"),
]

# Create output directory
output_dir = "batch_output"
os.makedirs(output_dir, exist_ok=True)

print("Processing molecules in batch mode...")
for smiles, name in molecules:
    try:
        output_path = os.path.join(output_dir, f"{name}.png")
        smiles_to_file(smiles, output_path, img_size=(400, 400))
        print(f"Processed: {name:20s} -> {output_path}")
    except Exception as e:
        print(f"Error processing {name:20s}: {e}")

print(f"\nBatch processing complete. Output directory: {output_dir}/")
