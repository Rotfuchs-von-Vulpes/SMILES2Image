from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smiles-to-image",
    version="0.1.1",
    author="tsiyukino",
    author_email="",
    description="Convert SMILES chemical notation to molecular structure images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsiyukino/SMILES2Image",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="smiles chemistry molecular structure cheminformatics rdkit",
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
    project_urls={
        "Bug Reports": "https://github.com/tsiyukino/SMILES2Image/issues",
        "Source": "https://github.com/tsiyukino/SMILES2Image",
    },
)
