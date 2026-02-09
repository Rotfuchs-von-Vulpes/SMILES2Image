"""
Command-line interface for SMILES to image conversion.
"""

import argparse
import sys
from .converter import smiles_to_file, smiles_to_image


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert SMILES chemical notation to molecular structure images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert SMILES to PNG file
  smiles2img "CCO" -o ethanol.png

  # Convert to JPEG with custom size
  smiles2img "c1ccccc1" -o benzene.jpg -f JPEG -s 500 500

  # Output to stdout (for piping)
  smiles2img "CCO" -f PNG --stdout > molecule.png

  # Read SMILES from file (one per line) and batch convert
  smiles2img --batch input.txt -o output_dir -f PNG
        """
    )

    parser.add_argument(
        "smiles",
        nargs="?",
        help="SMILES string to convert (required unless --batch is used)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path or directory (for batch mode)"
    )

    parser.add_argument(
        "-f", "--format",
        default="PNG",
        choices=["PNG", "JPEG", "JPG", "SVG"],
        help="Output image format (default: PNG)"
    )

    parser.add_argument(
        "-s", "--size",
        nargs=2,
        type=int,
        default=[300, 300],
        metavar=("WIDTH", "HEIGHT"),
        help="Image size in pixels (default: 300 300)"
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Output image bytes to stdout instead of file"
    )

    parser.add_argument(
        "--batch",
        metavar="INPUT_FILE",
        help="Batch process SMILES from file (one per line)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.batch and not args.smiles:
        parser.error("Either provide SMILES string or use --batch with input file")

    if args.batch and not args.output:
        parser.error("--batch mode requires --output directory")

    try:
        if args.batch:
            # Batch processing mode
            import os
            os.makedirs(args.output, exist_ok=True)

            with open(args.batch, 'r') as f:
                for idx, line in enumerate(f, 1):
                    smiles = line.strip()
                    if not smiles or smiles.startswith('#'):
                        continue

                    # Generate filename
                    filename = f"molecule_{idx}.{args.format.lower()}"
                    output_path = os.path.join(args.output, filename)

                    try:
                        smiles_to_file(smiles, output_path, args.format, tuple(args.size))
                        print(f"Converted: {smiles} -> {output_path}", file=sys.stderr)
                    except Exception as e:
                        print(f"Error converting '{smiles}': {e}", file=sys.stderr)

        elif args.stdout:
            # Output to stdout
            img_data = smiles_to_image(args.smiles, args.format, tuple(args.size))
            sys.stdout.buffer.write(img_data)

        else:
            # Single file output
            if not args.output:
                parser.error("--output is required unless using --stdout")

            output_path = smiles_to_file(args.smiles, args.output, args.format, tuple(args.size))
            print(f"Image saved to: {output_path}", file=sys.stderr)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
