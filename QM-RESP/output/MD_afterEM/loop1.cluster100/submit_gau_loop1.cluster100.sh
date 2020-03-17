#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 skx nodes
#----------------------------------------------------

#SBATCH -J loop1.cluster100
#SBATCH -o loop1.cluster100.o%j
#SBATCH -e loop1.cluster100.e%j
#SBATCH -p long
#SBATCH -N 1
#SBATCH -n 20
#SBATCH -t 48:00:00

module load gaussian16
export GAUSS_SCRDIR=$SLURM_SUBMIT_DIR

g16 < loop1.cluster100.inp > loop1.cluster100.log
