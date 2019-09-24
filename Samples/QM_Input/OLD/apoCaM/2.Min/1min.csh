#!/bin/csh  -f

################################################################################
##  This script is to prepare the files for atomistic simulations using       ##
##  GROMACS, including a short energy minimization, followed by NVT and NPT   ##
##  equilibrations. 							      ##
##  input : NNN.pdb em-vac-pme.mdp em-sol-pme.mdp nvt-pr-md.mdp npt-pr-md.mdp ##
##  output: NNN.top *.gro em-vac.tpr em-sol.tpr				      ##
##  By Pengzhi 5/12/2014						      ##
################################################################################

if ($#argv != 3) then
        echo "Usage:   		./Prep.csh  pdb		FF                  CA" 
        echo "Example: 		./Prep.csh  252		amber99sb-ildn      3"	
    endif

set pdb = $argv[1] 
set FF = $argv[2]
set ca = $argv[3]

module load gromacs

gmx editconf -f $pdb.gro -o $pdb-PBC.gro -bt cubic -c -princ -box 10 10 10 -d 1.0 -n protein.ndx 
gmx grompp -f em-vac-pme.mdp -c $pdb-PBC.gro -p $pdb.top -o em-vac.tpr
gmx mdrun -v -deffnm em-vac

