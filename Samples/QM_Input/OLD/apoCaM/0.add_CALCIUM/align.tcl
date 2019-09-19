# align.tcl: 
# align the Calcium binding loops in apoCaM and holoCaM
# to put the Calcium in the apoCaM loops
# author: Pengzhi Zhang, 12/18/2018

set crdfile0 1CFD.pdb
set crdfile1 1CLL.pdb
set molid0 [mol load pdb $crdfile0]
set molid1 [mol load pdb $crdfile1]

# loop1 20-31
set loop1 [atomselect $molid0 "resid 20 to 31 and name CA"]
set loop1C [atomselect $molid1 "resid 20 to 31 and name CA"]
set CA1 [atomselect $molid1 "index 1165"]
$CA1 move [measure fit $loop1C $loop1]
$CA1 writepdb "CA1.pdb"

# loop2 56-67
set loop2 [atomselect $molid0 "resid 56 to 67 and name CA"]
set loop2C [atomselect $molid1 "resid 56 to 67 and name CA"]
set CA2 [atomselect $molid1 "index 1166"]
$CA2 move [measure fit $loop2C $loop2]
$CA2 writepdb "CA2.pdb"

# loop3 93-104
set loop3 [atomselect $molid0 "resid 93 to 104 and name CA"]
set loop3C [atomselect $molid1 "resid 93 to 104 and name CA"]
set CA3 [atomselect $molid1 "index 1167"]
$CA3 move [measure fit $loop3C $loop3]
$CA3 writepdb "CA3.pdb"

# loop5 129-140
set loop4 [atomselect $molid0 "resid 129 to 140 and name CA"]
set loop4C [atomselect $molid1 "resid 129 to 140 and name CA"]
set CA4 [atomselect $molid1 "index 1168"]
$CA4 move [measure fit $loop4C $loop4]
$CA4 writepdb "CA4.pdb"

quit
