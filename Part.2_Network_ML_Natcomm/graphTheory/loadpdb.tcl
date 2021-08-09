proc loadfiles {} {
  display update off
  set pdblist [glob *.pdb]
  foreach pdb $pdblist {
    #if {[lindex $pdblist 0]==$pdb} {
      catch {mol new $pdb}
   # } else {
    #  animate read pdb $pdb
   # }
  }
}
proc completefiles {x} {
  set pdblist [glob *.pdb]
  for {set n 0} {$n< [expr [llength $pdblist]-$x]} {incr n} {
    mol new [lindex $pdblist [expr $n+$x]]
  }
}