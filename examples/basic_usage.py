"""
Basic usage examples for the smiles_to_image module.

This script demonstrates the core functionality of the SMILEStoImage library,
including file output, byte output, PIL Image manipulation, format conversion,
and custom sizing.
"""

from smiles_to_image import smiles_to_image, smiles_to_file
from PIL import Image

# Example 1: Save directly to file
print("Example 1: Save directly to file")
smiles_to_file("CCO", "ethanol.png")
print("Saved ethanol.png")

# Example 2: Get image as bytes
print("\nExample 2: Get image as bytes")
img_bytes = smiles_to_image("c1ccccc1", "PNG")
print(f"Generated {len(img_bytes)} bytes of PNG data")

# Example 3: Get PIL Image for further processing
print("\nExample 3: Get PIL Image and manipulate")
img = smiles_to_image("CC(=O)O", "PNG", return_pil=True)
img_rotated = img.rotate(45)
img_rotated.save("acetic_acid_rotated.png")
print("Saved rotated image")

# Example 4: Different formats
print("\nExample 4: Different image formats")
smiles_to_file("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "caffeine.jpg", "JPEG")
smiles_to_file("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "caffeine.svg", "SVG")
print("Saved JPEG and SVG versions")

# Example 5: Custom size
print("\nExample 5: Custom image size")
smiles_to_file("c1ccccc1", "benzene_large.png", img_size=(800, 800))
print("Saved large image (800x800)")

print("\nAll examples completed successfully")
