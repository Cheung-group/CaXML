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
        echo "Usage:   		$0  pdb		FF                  CA" 
        echo "Example: 		$0  252		amber99sb-ildn      3"	
	goto Done
    endif

set pdb = $argv[1] 
set FF = $argv[2]
set ca = $argv[3]

source /etc/profile.d/modules.csh
module purge
module load gromacs

echo 0 > Ca3.tem
echo 14 >> Ca3.tem
echo 0 >> Ca3.tem
echo 0 > Ca4.tem
echo 15 >> Ca4.tem
echo 0 >> Ca4.tem

gmx editconf -f $pdb.gro -o $pdb-PBC.gro -bt cubic -c -princ -box 10 10 10 -d 1.0 -n protein.ndx < Ca$ca.tem


## 2. energy minimization in vacuum
gmx grompp -f em-vac-pme.mdp -c $pdb-PBC.gro -p $pdb.top -o em-vac.tpr
gmx mdrun -v -deffnm em-vac
## 3. fill the periodic box with water
gmx solvate -cp em-vac.gro -cs spc216.gro -p $pdb.top -o $pdb-b4ion.gro
gmx grompp -f em-sol-pme.mdp -c $pdb-b4ion.gro -p $pdb.top -o ion.tpr

## 4. add ions 
echo 15 > tem
gmx genion -s ion.tpr -o $pdb-b4em.gro  -pname K -nname CL -neutral -conc 0.15 -p $pdb.top < tem 
rm -f tem

## 5. energy minimization for the solvent
gmx grompp -f em-sol-pme.mdp -c $pdb-b4em.gro -p $pdb.top -o em-sol.tpr
gmx mdrun -ntmpi 2 -ntomp 3 -gpu_id 01 -v -deffnm em-sol

Done:  
    exit
