#!/bin/csh 

set pdb = $argv[1] 


cat > save.tcl << EOF
set sel [atomselect top all]
\$sel writepdb min.$pdb.pdb
quit
EOF

vmd -dispdev text em-vac.gro -e save.tcl
