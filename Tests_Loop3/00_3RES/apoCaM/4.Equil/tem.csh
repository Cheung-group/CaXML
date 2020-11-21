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
	goto DONE
endif

set pdb = $argv[1] 
set FF = $argv[2]
set ca = $argv[3]

source /etc/profile.d/modules.csh
module purge
module load gromacs


# Problem here.
# equilibration in npt and protein position are restrained
gmx grompp -f npt-pr-md.mdp -c nvt-pr.gro -t nvt-pr.cpt -p $pdb.top -o npt-pr.tpr
gmx mdrun -ntmpi 2 -ntomp 3 -gpu_id 01 -v -deffnm npt-pr

# equilibration in npt and protein sidechains are flexible
gmx grompp -f npt-nopr-md.mdp -c npt-pr.gro -t npt-pr.cpt -p $pdb.top -o npt-nopr.tpr
gmx mdrun -ntmpi 2 -ntomp 3 -gpu_id 01 -v -deffnm npt-nopr

DONE:
    exit 0
