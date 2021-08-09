
# trajectory analysis
# optional parameters: start and endframe in the trajectory
# frames are numbered from 0
# usage: fResPair "sel1" "sel2" cutoff <startframe <endframe>>
#
# example:
# fResPair "protein" "resname CL" 3 0 0
# find all CL residues within 3A of protein in first frame
# example2:
# fResPair "protein" "resname CL" 3 10 20
# analogous, only perform analysis from frames 11 to 21
#
# prints output to 4 files:
# contact_all.dat
# 1 line per contact and frame
# frame number, contacting residues, minimal distance
# contactAB.dat
# 1 line per residue pair
# contacting residues, number of frames
# when these residues were in contact and percentage of
# the analyzed trajectory
# contactA.dat, contactB.dat
# 1 line per residue
# total number of contacts for each residue + percentage
# percentage values: 1 residue is expected to have max.
# 1 contact in 1 frame; i.e. percentage = contacts/frames
# these values can be misleading, since 1 res from groupA can interact
# with 2 residues from groupB - depending on size and character
# of the residues
# example:
# protein residues 1 (ARG), 5 (LYS) are in contact with 10 (CL)
# contact_all.dat: 1 1 ARG - 10 CL 3.50000
# 1 5 LYS - 10 CL 2.90000
# contact_AB.dat: 1 ARG - 10 CL 100% (1 frame(s))
# 5 LYS - 10 CL 100% (1 frame(s))
# contactA.dat 1 ARG - 100% (1 contact(s))
# 5 LYS - 100% (1 contact(s))
# contactB.dat 10 CL - 200% (2 contact(s))
#
proc fResPair { sel1 sel2 cutoff} {
  # get index of the last frame
  set numframes [expr [llength [molecule list]]/6]
  puts "total number of frames: $numframes"
  puts "analysis will be performed on $numframes frame(s)"
  
  # output file for printing out all contacts
  set fileAll "contact_all.dat"
  set fall [open $fileAll w+]
  
  # cycle over the trajectory
  for {set d 0} {$d< $numframes} {incr d} {
    
    # make some mappings
    set all [atomselect $d all]
    # resid map for every atom
    set allResid [$all get resid]
    # resname map for every atom
    set allResname [$all get resname]
    # create resid->resname map
    foreach resID $allResid resNAME $allResname {
     set mapResidResname($resID) $resNAME
    }
    # update selections
    # create specified atom selections
    set A [atomselect $d $sel1]
    set B [atomselect $d $sel2]
    # position for every atom
    set allPos [$all get {x y z}]
    
    # extract the pairs. listA and listB hold corresponding pairs from selections 1 and 2, respectively.
    foreach {listA listB} [measure contacts $cutoff $A $B] break
    
    #reflect list for contact symmetry
    set tempA $listA
    set listA [join [lappend listA $listB]]
    set listB [join [lappend listB $tempA]]

    # go through the pairs, assign distances
    foreach indA $listA indB $listB {
      # calculated distance between 2 atoms
      set dist [vecdist [lindex $allPos $indA] [lindex $allPos $indB]]

      # get information about residue id's
      set residA [lindex $allResid $indA]
      set residB [lindex $allResid $indB]
      # following code can be uncommented for testing purposes
      #set resnameA [lindex $allResname $indA]
      #set resnameB [lindex $allResname $indB]
      #puts "$residA $resnameA $residB $resnameB $dist"

      # results will be stored in [residA,residB][list of distances] array
      lappend contactTable($residA,$residB) $dist
    }

    foreach name [array names contactTable] {
      # assign residue names to residue numbers
      foreach {residA residB} [split $name ,] break
      foreach {tmp resnameA} [split [array get mapResidResname $residA] ] break
      foreach {tmp resnameB} [split [array get mapResidResname $residB] ] break
      # get minimum contact distance for the pair
      foreach {tmp distanceList} [array get contactTable $name] break
      set minDistance [lindex [lsort -real $distanceList] 0]

      # print to output file
      puts $fall [format "%-5d %5d %3s - %5d %3s - %f" $d $residA $resnameA $residB $resnameB $minDistance]
      flush $fall

      # store all contacts for residue pair (whole trajectory)
      lappend contactAB($residA,$residB) $minDistance
    }
    # delete the contact table - will be created again in the next loop
    if {[info exists contactTable]} {
      unset contactTable
    }
  }
  close $fall

  # open output files
  set fContAB "contact_AB.dat"
  set fcAB [open $fContAB w+]

  foreach name [array names contactAB] {
    foreach {residA residB} [split $name ,] break
    foreach {tmp resnameA} [split [array get mapResidResname $residA] ] break
    foreach {tmp resnameB} [split [array get mapResidResname $residB] ] break
    set frames [llength $contactAB($name)]
    set percentage [expr 100.0 * $frames / $numframes]
    puts $fcAB [format "%5d %3s - %5d %3s - %6.3f %% (%d frame(s))" $residA $resnameA $residB $resnameB $percentage $frames]
    flush $fcAB
  }
  # close output files
  close $fcAB

  puts "done"
} 
