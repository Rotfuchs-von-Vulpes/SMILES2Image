"""
Core conversion functions for SMILES to molecular structure image conversion.

This module contains the primary conversion logic for transforming SMILES notation
into graphical representations of molecular structures using RDKit.
"""

import io
import re
import cairosvg
from io import BytesIO
from typing import Optional, Tuple, Union
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image


def smiles_to_image(
    smiles: str,
    img_format: str = "PNG",
    img_size: Tuple[int, int] = (300, 300),
    return_pil: bool = False
) -> Union[bytes, Image.Image]:
    """
    Convert a SMILES string to a molecular structure image.

    This function parses a SMILES notation and generates a 2D molecular structure
    representation. The output can be returned as raw bytes for file I/O and network
    transmission, or as a PIL Image object for further image processing operations.

    Args:
        smiles: SMILES string representation of the molecule.
        img_format: Output image format. Supported formats include PNG, JPEG, and SVG.
                   Default is PNG.
        img_size: Image dimensions as (width, height) tuple in pixels. Default is (300, 300).
        return_pil: If True, returns a PIL Image object instead of bytes. Default is False.

    Returns:
        Image data in the specified format as bytes (default), or a PIL Image object
        if return_pil is True.

    Raises:
        ValueError: If the SMILES string is invalid or cannot be parsed by RDKit.

    Examples:
        Basic usage returning bytes:
        >>> img_bytes = smiles_to_image("CCO", "PNG")

        Returning PIL Image for further processing:
        >>> img = smiles_to_image("CCO", "PNG", return_pil=True)
        >>> img.save("output.png")

        Custom format and size:
        >>> img_bytes = smiles_to_image("c1ccccc1", "JPEG", (500, 500))
    """
    # Parse SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")

    # Generate the molecule image
    drawer = rdMolDraw2D.MolDraw2DSVG(img_size[0], img_size[1])
    opts = drawer.drawOptions()
    opts.clearBackground = False 
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()

    svg = drawer.GetDrawingText()
    svg = re.sub(r"#000000", "#FFFFFF", svg, flags=re.IGNORECASE)
    svg = re.sub(r"black", "white", svg, flags=re.IGNORECASE)
    png_data = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")

    # Return PIL Image if requested
    if return_pil:
        return img

    # Convert to bytes
    img_buffer = BytesIO()
    img_format_upper = img_format.upper()

    # Handle format-specific settings
    if img_format_upper == "JPEG" or img_format_upper == "JPG":
        # JPEG doesn't support transparency, convert RGBA to RGB
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        img.save(img_buffer, format="JPEG", quality=95)
    elif img_format_upper == "SVG":
        # For SVG, use RDKit's SVG drawer
        from rdkit.Chem import Draw as ChemDraw
        drawer = ChemDraw.rdMolDraw2D.MolDraw2DSVG(img_size[0], img_size[1])
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg_content = drawer.GetDrawingText()
        return svg_content.encode('utf-8')
    else:
        img.save(img_buffer, format=img_format_upper)

    return img_buffer.getvalue()


def smiles_to_file(
    smiles: str,
    output_path: str,
    img_format: Optional[str] = None,
    img_size: Tuple[int, int] = (300, 300)
) -> str:
    """
    Convert a SMILES string to an image file.

    This convenience function combines SMILES to image conversion with file I/O
    operations. The image format can be explicitly specified or automatically
    inferred from the file extension.

    Args:
        smiles: SMILES string representation of the molecule.
        output_path: File system path where the image will be saved.
        img_format: Output image format. If None, the format is inferred from the
                   file extension of output_path. Default is None.
        img_size: Image dimensions as (width, height) tuple in pixels. Default is (300, 300).

    Returns:
        The path to the saved file.

    Raises:
        ValueError: If the SMILES string is invalid or the image format cannot be
                   determined from the filename when img_format is None.

    Examples:
        Format automatically inferred from file extension:
        >>> smiles_to_file("CCO", "ethanol.png")
        'ethanol.png'

        Explicit format specification:
        >>> smiles_to_file("c1ccccc1", "benzene.img", img_format="JPEG")
        'benzene.img'
    """
    # Infer format from file extension if not provided
    if img_format is None:
        import os
        _, ext = os.path.splitext(output_path)
        if not ext:
            raise ValueError("Cannot infer image format from filename. Please provide img_format parameter.")
        img_format = ext[1:]  # Remove the dot

    # Get image bytes
    img_data = smiles_to_image(smiles, img_format, img_size)

    # Write to file
    mode = 'wb' if isinstance(img_data, bytes) else 'w'
    with open(output_path, mode) as f:
        f.write(img_data)

    return output_path
