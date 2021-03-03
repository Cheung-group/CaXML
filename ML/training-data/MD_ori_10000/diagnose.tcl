set sys         [atomselect top "all"]
set pro         [atomselect top "protein"]

set nf [molinfo top get numframes]
for {set i 1} {$i < $nf} {incr i} {
    set bondl [measure rgyr "$sys" frame $i]
    puts $bondl
    set prot [measure rgyr "$pro" frame $i]
    if {$bondl/$pro > 1.3 or $bondl/$pro < 0.7} {
        puts "BREAK IN THE BONDS at frame $i"
    }
}

quit
