# Computational Design of Low-Volatility Lubricants for Space Using Interpretable Machine Learning

This repository contains sample code and data associated with the manuscript *Computational Design of Low-Volatility Lubricants for Space Using Interpretable Machine Learning*. Some scripts are standalone adaptations of those used in automated workflows. 

## Manuscript

**Computational Design of Low-Volatility Lubricants for Space Using Interpretable Machine Learning**

[[arXiv]](https://arxiv.org/abs/2512.05870) 

**Authors**:
- Daniel Miliate - dmiliate@ucmerced.edu
- Ashlie Martini - amartini@ucmerced.edu

## Acknowledgments
This project uses code from the Substructure-Mask-Explanation implementation:
Wu, Z., Wang, J., Du, H. et al. Chemistry-intuitive explanation of graph neural networks for molecular property prediction with substructure masking. Nat Commun 14, 2585 (2023). [https://doi.org/10.1038/s41467-023-38192-3](https://doi.org/10.1038/s41467-023-38192-3)

Modifications: The repo has been cloned with minimal modification for demostrated use. 

Github: [https://github.com/wzxxxx/Substructure-Mask-Explanation](https://github.com/wzxxxx/Substructure-Mask-Explanation)

License: [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)

---

This project uses code from the PyL3dMD implementation:
Panwar, P., Yang, Q. & Martini, A. PyL3dMD: Python LAMMPS 3D molecular descriptors package. J Cheminform 15, 69 (2023). [https://doi.org/10.1186/s13321-023-00737-5](https://doi.org/10.1186/s13321-023-00737-5)

Modifications: Minor modifications have been made to the pyl3dmd.py file, commented with "EDIT: [description]"

Github: [https://github.com/panwarp/PyL3dMD](https://github.com/panwarp/PyL3dMD)

License: [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Python Environment
PyL3dMD and SME repos may conflict, and users may want to install in separate environments. Regardless, install instructions have been made available.

```bash
# Clone the repository
git clone https://github.com/Dmiliate2/ML4VP.git
cd ML4VP

# Create conda environment
conda create --name ML4VP python=3.7
conda activate ML4VP

# Install most requirements 
pip install -r requirements.txt

# Add dgl and torch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install dgl -f https://data.dgl.ai/wheels/cu117/repo.html

# Apply patch
python apply_PyL3dMD_patch.py

```

Alternative 

```bash
# Clone the repository
git clone https://github.com/Dmiliate2/ML4VP.git
cd ML4VP

# Create conda environment
conda env create -f ML4VP.yml
conda activate ML4VP

# Apply patch
python apply_PyL3dMD_patch.py

```


## Datasets

The models are trained on:

- **460 unique molecules** from NIST Chemistry WebBook
- **2 MAC molecules** from available reports
- **9,240 vapor pressure instances** (variable temperature)
- **337 molecules at 387K** (fixed temperature)
- Chemistries: H/C, H/C/O, H/C/F, C/F, H/C/O/F


## Molecular Dynamics Simulations

MD simulations for dynamic descriptors are performed using LAMMPS with:

- Force field: OPLS-AA
- Dynamic Features: Radius of gyration, density, HATS descriptors...
- Static Features: Molecular weight, # Carbon atoms, Bertz...

## Contributing

We welcome contributions and suggestions. Please feel free to submit a Pull Request or open an issue for major changes to discuss your proposal. While all feedback is appreciated, we may not be able to incorporate every change.


**Note:** This repository is under active development. Some features may be added or modified as the project evolves.


