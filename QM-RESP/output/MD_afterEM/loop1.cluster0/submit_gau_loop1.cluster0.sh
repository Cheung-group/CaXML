#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 skx nodes
#----------------------------------------------------

#SBATCH -J loop1.cluster0
#SBATCH -o loop1.cluster0.o%j
#SBATCH -e loop1.cluster0.e%j
#SBATCH -p skx-normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 12:00:00
#SBATCH -A TG-MCB190109

module load gaussian

tmpdir=$SCRATCH/$SLURM_JOB_ID
mkdir $tmpdir
export GAUSS_SCRDIR=$tmpdir

g16 < loop1.cluster0.inp > loop1.cluster0.log
