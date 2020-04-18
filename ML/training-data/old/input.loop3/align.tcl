# align.tcl: align the crd with given native structure
# usage: vmd -dispdev text -e align.tcl -agrs ref.pdb ori.pdb
# author: Pengzhi Zhang, 7/27/2011

set crdfile0 [lindex $argv 0]
set crdfile1 [lindex $argv 1]
set outfile [open $crdfile1.aligned w]

set molid0 [mol load pdb $crdfile0]
set molid1 [mol load pdb $crdfile1]
set sel0 [atomselect $molid0 "protein and mass > 1.1"]
set sel1 [atomselect $molid1 "protein and mass > 1.1"]
set sel [atomselect $molid1 "all"]

$sel move [measure fit $sel1 $sel0]

animate write pdb $crdfile1.aligned waitfor all $molid1
close $outfile
quit
