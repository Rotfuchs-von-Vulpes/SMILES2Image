# SMILEStoImage

A Python library for converting SMILES (Simplified Molecular Input Line Entry System) chemical notation to molecular structure images.

## Overview

SMILEStoImage provides a programmatic interface for generating 2D molecular structure visualizations from SMILES strings. The library is built on RDKit and supports multiple output formats suitable for web services, data processing pipelines, and cheminformatics applications.

## Features

- Convert SMILES notation to molecular structure images
- Multiple output formats: PNG, JPEG, SVG
- Flexible return types: raw bytes or PIL Image objects
- Configurable image dimensions
- Command-line interface for batch processing
- Minimal dependencies

## Installation

### Requirements

- Python 3.8 or higher
- RDKit 2023.9.1 or higher
- Pillow 10.0.0 or higher

### From Source

```bash
git clone https://github.com/tsiyukino/SMILEStoImage.git
cd SMILEStoImage
pip install -r requirements.txt
pip install -e .
```

## Usage

### Python API

#### Basic Conversion

```python
from smiles_to_image import smiles_to_image, smiles_to_file

# Save directly to file
smiles_to_file("CCO", "ethanol.png")

# Get image as bytes
img_bytes = smiles_to_image("c1ccccc1", "PNG")

# Get PIL Image object for further processing
img = smiles_to_image("CCO", "PNG", return_pil=True)
img.save("output.png")
```

#### Advanced Usage

```python
# Specify custom image size
smiles_to_file("c1ccccc1", "benzene.png", img_size=(800, 800))

# Convert to different formats
smiles_to_file("CCO", "ethanol.jpg", img_format="JPEG")
smiles_to_file("CCO", "ethanol.svg", img_format="SVG")

# Get bytes for network transmission
img_bytes = smiles_to_image("CC(=O)O", "PNG", img_size=(500, 500))
```

### Command-Line Interface

The library includes a command-line tool for standalone usage and batch processing.

#### Basic Usage

```bash
# Convert single SMILES string
smiles2img "CCO" -o ethanol.png

# Specify format and size
smiles2img "c1ccccc1" -o benzene.jpg -f JPEG -s 600 600

# Output to stdout
smiles2img "CCO" -f PNG --stdout > molecule.png
```

#### Batch Processing

```bash
# Create input file with one SMILES per line
cat > molecules.txt << EOF
CCO
c1ccccc1
CC(=O)O
EOF

# Process batch
smiles2img --batch molecules.txt -o output_directory -f PNG
```

## API Reference

### smiles_to_image()

```python
smiles_to_image(smiles, img_format="PNG", img_size=(300, 300), return_pil=False)
```

Convert a SMILES string to a molecular structure image.

**Parameters:**
- `smiles` (str): SMILES string representation of the molecule.
- `img_format` (str): Output format (PNG, JPEG, SVG). Default: "PNG".
- `img_size` (tuple): Image dimensions as (width, height) in pixels. Default: (300, 300).
- `return_pil` (bool): Return PIL Image object instead of bytes. Default: False.

**Returns:**
- `bytes` or `PIL.Image.Image`: Image data in specified format (bytes by default).

**Raises:**
- `ValueError`: If SMILES string is invalid.

### smiles_to_file()

```python
smiles_to_file(smiles, output_path, img_format=None, img_size=(300, 300))
```

Convert a SMILES string to an image file.

**Parameters:**
- `smiles` (str): SMILES string representation of the molecule.
- `output_path` (str): File path for the output image.
- `img_format` (str, optional): Output format. If None, inferred from file extension.
- `img_size` (tuple): Image dimensions as (width, height) in pixels. Default: (300, 300).

**Returns:**
- `str`: Path to the saved file.

**Raises:**
- `ValueError`: If SMILES string is invalid or format cannot be determined.

## Integration Examples

### Web Service Integration

```python
from flask import Flask, send_file
from io import BytesIO
from smiles_to_image import smiles_to_image

app = Flask(__name__)

@app.route('/molecule/<smiles>')
def get_molecule(smiles):
    img_bytes = smiles_to_image(smiles, "PNG")
    return send_file(BytesIO(img_bytes), mimetype='image/png')
```

### Batch Processing

```python
from smiles_to_image import smiles_to_file

molecules = [
    ("CCO", "ethanol"),
    ("c1ccccc1", "benzene"),
    ("CC(=O)O", "acetic_acid")
]

for smiles, name in molecules:
    smiles_to_file(smiles, f"{name}.png", img_size=(400, 400))
```

### Data Pipeline Integration

```python
from smiles_to_image import smiles_to_image

# Generate fixed-size images for machine learning applications
training_data = []
for smiles in smiles_list:
    img_bytes = smiles_to_image(smiles, "PNG", img_size=(224, 224))
    training_data.append(img_bytes)
```

## Common SMILES Examples

| Molecule      | SMILES                                |
|---------------|---------------------------------------|
| Ethanol       | CCO                                   |
| Benzene       | c1ccccc1                              |
| Acetic acid   | CC(=O)O                               |
| Caffeine      | CN1C=NC2=C1C(=O)N(C(=O)N2C)C         |
| Aspirin       | CC(=O)Oc1ccccc1C(=O)O                |

## Project Structure

```
SMILEStoImage/
├── smiles_to_image/
│   ├── __init__.py       # Package initialization
│   ├── converter.py      # Core conversion logic
│   └── cli.py           # Command-line interface
├── examples/            # Integration examples
├── tests/              # Unit tests
├── setup.py            # Package configuration
└── requirements.txt    # Dependencies
```

## Development

### Running Tests

```bash
pip install pytest
pytest tests/
```

### Installing in Development Mode

```bash
pip install -e .
```

## Technical Details

### Image Generation

The library uses RDKit's molecular visualization capabilities to generate 2D structure diagrams. For raster formats (PNG, JPEG), the conversion pipeline is:

1. Parse SMILES string using RDKit
2. Generate 2D coordinates
3. Render to PIL Image
4. Convert to requested format

For SVG output, RDKit's native SVG renderer is used directly.

### Format-Specific Handling

- **PNG**: Direct PIL output with transparency support
- **JPEG**: RGBA to RGB conversion with white background
- **SVG**: Vector output using RDKit's SVG drawer

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome. Please ensure that:

1. Code follows existing style conventions
2. All tests pass
3. New features include appropriate tests
4. Documentation is updated accordingly

## Support

For bug reports and feature requests, please use the GitHub issue tracker.
