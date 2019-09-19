# Read in the frame of the selected loop.

set cluster [lindex $argv 0]
set frame [lindex $argv 1]
puts "frame $frame"
set loop3 [atomselect top "resid 93 to 104"]
set ca3 [atomselect top "resid 151"]
set idxca3 [$ca3 get index]
set nearbyOW [atomselect top "name OW and within 3 of resid 151" frame $frame]
set idxnearbyOW [$nearbyOW get index]

puts "ca index $idxca3"
puts "nearby water index $idxnearbyOW"

# find the nearest water around the 3rd Ca2+ 
#set mindist 3.1
#set nearestOW [lindex $idxnearbyOW 0]
for {set i 0} {$i < [llength $idxnearbyOW]} {incr i} {
#    set idxOW [lindex $idxnearbyOW $i]
#    set dist [measure bond [list $idxOW $idxca3] frame $frame]
#    puts "comparing dist $dist with current min $mindist"
#    if {$dist < $mindist} {
#        set mindist $dist
#        set nearestOW $idxOW
#    }

    set idxOW [lindex $idxnearbyOW $i]
    set sel3 [atomselect top "index $idxOW"]
    set idx3 [$sel3 get resid]
    set sel [atomselect top "resid 93 to 104 or resid 151 $idx3" frame $frame]
    $sel writepdb $cluster.$i.pdb 

}

#puts "Nearest OW is index $nearestOW within $mindist of Ca2+"
    
#set sel1 [atomselect top "resid 93 95 104"]
#set idx1 [$sel1 get index]
#set sel2 [atomselect top "resid 93 95 104 and sidechain"] 
#set idx2 [$sel2 get index]
#set sel3 [atomselect top "index $nearestOW"]
#set idx3 [$sel3 get resid]
#set sel [atomselect top "resid 93 to 104 or resid 151 $idx3" frame $frame]
#$sel writepdb $cluster.pdb 
quit
