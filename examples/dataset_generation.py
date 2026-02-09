"""
Dataset generation example.

This example demonstrates how to use the converter to create structured
datasets with molecular structure images and associated metadata.
"""

import os
import json
from smiles_to_image import smiles_to_image
import base64

# Sample dataset (in practice, this would come from a database or file)
# Format: (SMILES, properties/labels)
training_data = [
    ("CCO", {"name": "ethanol", "class": "alcohol", "toxic": False}),
    ("c1ccccc1", {"name": "benzene", "class": "aromatic", "toxic": True}),
    ("CC(=O)O", {"name": "acetic_acid", "class": "carboxylic_acid", "toxic": False}),
    ("CC(C)O", {"name": "isopropanol", "class": "alcohol", "toxic": False}),
    ("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", {"name": "caffeine", "class": "alkaloid", "toxic": False}),
]


def create_image_dataset(output_dir="training_dataset", img_format="PNG", img_size=(224, 224)):
    """
    Create a dataset with images and metadata.

    Args:
        output_dir: Directory to save the dataset
        img_format: Image format (PNG, JPEG, etc.)
        img_size: Size of generated images (important for neural networks)
    """
    os.makedirs(output_dir, exist_ok=True)

    dataset_metadata = []

    print(f"Generating dataset in {output_dir}/...")
    for idx, (smiles, properties) in enumerate(training_data):
        try:
            # Generate image
            img_bytes = smiles_to_image(smiles, img_format, img_size)

            # Save image
            img_filename = f"molecule_{idx:04d}.{img_format.lower()}"
            img_path = os.path.join(output_dir, img_filename)
            with open(img_path, 'wb') as f:
                f.write(img_bytes)

            # Store metadata
            metadata = {
                "id": idx,
                "smiles": smiles,
                "image_file": img_filename,
                "properties": properties
            }
            dataset_metadata.append(metadata)

            print(f"Generated {img_filename} for {properties['name']}")

        except Exception as e:
            print(f"Error processing {smiles}: {e}")

    # Save metadata
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(dataset_metadata, f, indent=2)

    print(f"\nDataset created successfully!")
    print(f"  Images: {len(dataset_metadata)} files in {output_dir}/")
    print(f"  Metadata: {metadata_path}")

    return dataset_metadata


def create_embedded_dataset(output_file="embedded_dataset.json", img_format="PNG", img_size=(224, 224)):
    """
    Create a single JSON file with base64-encoded images.
    Useful for datasets that need to be portable or stored in databases.
    """
    dataset = []

    print(f"Generating embedded dataset...")
    for idx, (smiles, properties) in enumerate(training_data):
        try:
            # Generate image
            img_bytes = smiles_to_image(smiles, img_format, img_size)

            # Encode as base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

            # Create record
            record = {
                "id": idx,
                "smiles": smiles,
                "image_base64": img_base64,
                "image_format": img_format,
                "properties": properties
            }
            dataset.append(record)

            print(f"Encoded {properties['name']}")

        except Exception as e:
            print(f"Error processing {smiles}: {e}")

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"\nEmbedded dataset created: {output_file}")
    print(f"  Total size: {os.path.getsize(output_file) / 1024:.2f} KB")

    return dataset


if __name__ == "__main__":
    print("=== Dataset Generation Example ===\n")

    # Method 1: Separate image files with metadata
    print("Method 1: Separate files")
    create_image_dataset(img_size=(224, 224))

    print("\n" + "="*50 + "\n")

    # Method 2: Embedded base64 images
    print("Method 2: Embedded base64")
    create_embedded_dataset()

    print("\nDataset generation completed successfully!")
