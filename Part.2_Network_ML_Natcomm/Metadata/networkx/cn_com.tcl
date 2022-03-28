
set ion [atomselect top "resname CA"]
set prot [atomselect top "protein"]
set coor [atomselect top "(element O) and (within 3.0 of resname CA) and (not water)"]

set cn [$coor num]

set pos_ion [measure center $ion]
set com [measure center $prot weight mass]
set diff [vecsub $com $pos_ion]
set d [veclength $diff]
puts "NNN$cn $d"

quit

