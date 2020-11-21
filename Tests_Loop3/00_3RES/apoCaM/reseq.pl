#!/usr/bin/perl -w
################################################################################
# Modified by P. Zhang, 3/7/2014
################################################################################


$pdbfile = 'tem.pdb';
@array = ();
$j = 0;

open (OUT1,">New.pdb") or die "failed to open New_Atoms.pdb";
open (PDBFILE,"$pdbfile") or die "failed to open $pdbfile, ";

while (<PDBFILE>) {
	       $array[$j][0] = substr($_,0,6);
           $array[$j][1] = substr($_,6,6);   #atom index 
           $array[$j][2] = substr($_,12,62);  #rest
           $j++;
		 }

$num_of_tem=$j;

for ($j=0;$j<$num_of_tem;$j++)
{
    $array[$j][1]=$j+1;
    printf OUT1 "%6s%6d%s\n", $array[$j][0], $array[$j][1], $array[$j][2];
}
