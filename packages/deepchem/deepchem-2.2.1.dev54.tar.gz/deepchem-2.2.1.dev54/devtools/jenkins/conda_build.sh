#!/bin/bash
cd devtools/conda-recipe
source activate base
conda upgrade conda -y
conda install conda-build anaconda-client conda-verify -y
conda upgrade conda-build anaconda-client conda-verify -y
conda build purge
conda build deepchem -c defaults -c rdkit -c anaconda -c omnia -c conda-forge >> log.txt

unamestr=`uname`
if [[ "$unamestr" != 'Darwin' ]];
then
   export package_name=deepchem-gpu
   conda build deepchem -c defaults -c rdkit -c anaconda -c omnia -c conda-forge >> log.txt
fi
