proc loadfiles {} {
  display update off
  set pdblist [glob *.pdb]
  foreach pdb $pdblist {
    catch {mol new $pdb}
  }
}
proc completefiles {x} {
  set pdblist [glob *.pdb]
  for {set n 0} {$n< [expr [llength $pdblist]-$x]} {incr n} {
    mol new [lindex $pdblist [expr $n+$x]]
  }
}

proc recursiveLoad {x} {
  set pdblist [glob *.pdb]
  if {[llength $pdblist] == $x} {
    return
  }   
  mol new [lindex $pdblist $x]
  return [recursiveLoad [expr {$x + 1}]]
}