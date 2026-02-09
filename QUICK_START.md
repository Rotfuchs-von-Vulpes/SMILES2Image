# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### Python API

```python
from smiles_to_image import smiles_to_image, smiles_to_file

# Save to file
smiles_to_file("CCO", "ethanol.png")

# Get image bytes
img_bytes = smiles_to_image("CCO", "PNG")

# Get PIL Image object
img = smiles_to_image("CCO", return_pil=True)
```

### Command Line

```bash
smiles2img "CCO" -o ethanol.png
```

## Common Use Cases

### Web Service Integration

```python
from flask import send_file
from io import BytesIO
from smiles_to_image import smiles_to_image

img_bytes = smiles_to_image("CCO", "PNG")
return send_file(BytesIO(img_bytes), mimetype='image/png')
```

### Batch Processing

```python
from smiles_to_image import smiles_to_file

molecules = [("CCO", "ethanol"), ("c1ccccc1", "benzene")]
for smiles, name in molecules:
    smiles_to_file(smiles, f"{name}.png")
```

### Machine Learning Applications

```python
from smiles_to_image import smiles_to_image

# Generate fixed-size images for neural networks
img_bytes = smiles_to_image("CCO", "PNG", img_size=(224, 224))
```

## Examples

Complete integration examples are available in the `examples/` directory:

- `basic_usage.py` - API usage examples
- `batch_processing.py` - Batch conversion
- `web_api_integration.py` - Flask web service
- `ai_training_dataset.py` - Dataset generation
- `gui_integration.py` - Desktop application

To run an example:

```bash
cd examples
python basic_usage.py
```

## Common SMILES Strings

| Molecule      | SMILES                                |
|---------------|---------------------------------------|
| Ethanol       | CCO                                   |
| Benzene       | c1ccccc1                              |
| Acetic acid   | CC(=O)O                               |
| Caffeine      | CN1C=NC2=C1C(=O)N(C(=O)N2C)C         |

## Documentation

- Full API reference: README.md
- Code documentation: See docstrings in source files
