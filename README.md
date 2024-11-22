# CaXML
Deriving Ca2+ Charge in Varying Environments Using Machine Learning Methods

Input: PDB or MD structure of the EF-hand calcium-binding loop [12 residues + 1 calcium ion].

Output: i-RESP (or RESP) calcium charge in the given environment. 

# Required packages

- pymol # conda install -c conda-forge -c schrodinger pymol-bundle
- xgboost
- pandas
- networkx
- dscribe

**NOTE:**
_scipy_, _biopython_, and _scikit-learn_ are already installed as dependencies of the above packages.
