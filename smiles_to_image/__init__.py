"""
SMILEStoImage - SMILES to Molecular Structure Image Converter

This module provides an API for converting SMILES (Simplified Molecular Input Line
Entry System) strings to molecular structure images in various formats. The module
is designed for integration into cheminformatics workflows, web services, and
data processing pipelines.
"""

from .converter import smiles_to_image, smiles_to_file

__version__ = "0.1.0"
__all__ = ["smiles_to_image", "smiles_to_file"]
