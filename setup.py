from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smiles-to-image",
    version="0.1.0",
    author="SMILEStoImage Contributors",
    description="Convert SMILES chemical notation to molecular structure images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SMILEStoImage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rdkit>=2023.9.1",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "smiles2img=smiles_to_image.cli:main",
        ],
    },
)
