#!/bin/csh 

if ($#argv != 3) then
        echo "Usage:   		$0  pdb		FF                  CA" 
        echo "Example: 		$0  252		amber99sb-ildn      3"	
	goto DONE
    endif

set pdb = $argv[1] 
set FF = $argv[2]
set ca = $argv[3]

module load gromacs

## 1. prepare the pdb file 
sed -i "s/HSD/HIS/g;s/HSE/HIS/g" tem.pdb
sed -i "s/OT1/O\ \ /g;s/OT2/OXT/g" tem.pdb
sed -i "s/CAL/\ CA/g" tem.pdb 

gmx pdb2gmx -ignh -ff $FF -f tem.pdb -o $pdb.gro -p $pdb.top -posrefc 1000000 -water tip3p 

sed -i "s/POSRES/POSRES_CA/g" "$pdb"_Ion_chain_X2.itp

cat > inp << EOF
r 93-104 & 5
name 14 loop3
r 151
name 15 Ca3
q
EOF

gmx make_ndx -f $pdb.gro -o protein.ndx < inp

DONE:
    exit
