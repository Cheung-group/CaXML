# Script to find the distance 
# distance between Calcium and coordinating oxygens.
# angle between calcium and coordinating oxygens

	# get the number of frames
	set num_steps [molinfo top get numframes]

	# open file for writing
	set fil [open vectors.dat w]

    # get index of the atoms 
    set ca [atomselect top "resid 151"]
    set caidx [$ca get index]

    set ox [atomselect top "name \"O\.\*\"  and sidechain and resid 93 95 97 99 101 104"]
    set oxidx [$ox get index]

    set numOx [llength $oxidx]
    
	# loop over all frames in the trajectory
	for {set frame 0} {$frame < $num_steps} {incr frame} {
        set vec {}

        # for o-ca bonds
        foreach oxatom $oxidx {
            set bond [measure bond "$caidx $oxatom" frame $frame]
            lappend vec $bond
        }

        # for o-ca-o angles
        for {set i 0} {$i < $numOx} {incr i} {
            for {set j [expr {$i + 1}] } {$j < $numOx} {incr j} {
                set angle [measure angle "[lindex $oxidx $i] $caidx [lindex $oxidx $j]" frame $frame]
                lappend vec $angle
            }
        }

		puts $fil $vec
    }

close $fil
quit
