"""
Flask web API integration example.

This script demonstrates how to integrate the SMILEStoImage library into
a web service using Flask. The API accepts POST requests with SMILES strings
and returns molecular structure images.
"""

from flask import Flask, request, send_file, jsonify
from io import BytesIO
from smiles_to_image import smiles_to_image

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert_smiles():
    """
    API endpoint for SMILES to image conversion.

    Request JSON format:
    {
        "smiles": "CCO",
        "format": "PNG",
        "width": 300,
        "height": 300
    }

    Returns:
        Image file or JSON error response
    """
    try:
        data = request.get_json()
        smiles = data.get('smiles')

        if not smiles:
            return jsonify({'error': 'SMILES string is required'}), 400

        img_format = data.get('format', 'PNG').upper()
        width = data.get('width', 300)
        height = data.get('height', 300)

        # Convert SMILES to image
        img_bytes = smiles_to_image(smiles, img_format, (width, height))

        # Return image
        return send_file(
            BytesIO(img_bytes),
            mimetype=f'image/{img_format.lower()}',
            as_attachment=False
        )

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("Starting SMILES converter web API...")
    print("Example usage:")
    print('  curl -X POST http://localhost:5000/convert -H "Content-Type: application/json" -d \'{"smiles": "CCO"}\' --output molecule.png')
    app.run(debug=True, port=5000)
