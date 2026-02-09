"""
Unit tests for the SMILES converter module.
"""

import pytest
from PIL import Image
from smiles_to_image import smiles_to_image, smiles_to_file
import os
import tempfile


class TestSMILESToImage:
    """Test smiles_to_image function."""

    def test_valid_smiles_returns_bytes(self):
        """Test that valid SMILES returns bytes."""
        result = smiles_to_image("CCO", "PNG")
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_valid_smiles_returns_pil_image(self):
        """Test that return_pil=True returns PIL Image."""
        result = smiles_to_image("CCO", "PNG", return_pil=True)
        assert isinstance(result, Image.Image)

    def test_invalid_smiles_raises_error(self):
        """Test that invalid SMILES raises ValueError."""
        with pytest.raises(ValueError, match="Invalid SMILES"):
            smiles_to_image("INVALID_SMILES_123", "PNG")

    def test_different_formats(self):
        """Test different output formats."""
        smiles = "c1ccccc1"

        # PNG
        png_result = smiles_to_image(smiles, "PNG")
        assert isinstance(png_result, bytes)
        assert png_result[:8] == b'\x89PNG\r\n\x1a\n'  # PNG signature

        # JPEG
        jpg_result = smiles_to_image(smiles, "JPEG")
        assert isinstance(jpg_result, bytes)
        assert jpg_result[:2] == b'\xff\xd8'  # JPEG signature

        # SVG
        svg_result = smiles_to_image(smiles, "SVG")
        assert isinstance(svg_result, bytes)
        assert b'<svg' in svg_result or b'<?xml' in svg_result

    def test_custom_size(self):
        """Test custom image size."""
        img = smiles_to_image("CCO", "PNG", img_size=(500, 500), return_pil=True)
        assert img.size == (500, 500)

    def test_common_molecules(self):
        """Test conversion of common molecules."""
        molecules = [
            "CCO",  # Ethanol
            "c1ccccc1",  # Benzene
            "CC(=O)O",  # Acetic acid
            "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine
        ]

        for smiles in molecules:
            result = smiles_to_image(smiles, "PNG")
            assert isinstance(result, bytes)
            assert len(result) > 0


class TestSMILESToFile:
    """Test smiles_to_file function."""

    def test_save_to_file(self):
        """Test saving image to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            result = smiles_to_file("CCO", output_path)

            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0

    def test_format_inference_from_extension(self):
        """Test that format is inferred from file extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # PNG
            png_path = os.path.join(tmpdir, "test.png")
            smiles_to_file("CCO", png_path)
            assert os.path.exists(png_path)

            # JPEG
            jpg_path = os.path.join(tmpdir, "test.jpg")
            smiles_to_file("CCO", jpg_path)
            assert os.path.exists(jpg_path)

    def test_explicit_format(self):
        """Test explicit format parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.img")
            smiles_to_file("CCO", output_path, img_format="PNG")

            assert os.path.exists(output_path)

    def test_custom_size_file(self):
        """Test custom size when saving to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            smiles_to_file("CCO", output_path, img_size=(600, 600))

            assert os.path.exists(output_path)
            # Verify size by reading back
            img = Image.open(output_path)
            assert img.size == (600, 600)

    def test_no_extension_no_format_raises_error(self):
        """Test that missing extension and format raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test")
            with pytest.raises(ValueError, match="Cannot infer image format"):
                smiles_to_file("CCO", output_path)
