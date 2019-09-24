#!/usr/bin/perl -w

################################################################################
# Convert pdb to xyz
# format:
# Atom x y z
# %4s%1s%15.8f%15.8f%15.8f
# Modified by P. Zhang, 4/23/2019
################################################################################


use strict;
use warnings;

my $pdbfile = $ARGV[0];     # pdb file name

my @array = ();
my $j = 0;
my $name = '';

open (OUT,">New.xyz") or die "failed to open file for output New.xyz!";
open (PDBFILE,"$pdbfile") or die "failed to open $pdbfile, ";

while (<PDBFILE>) {
    $name = substr($_,0,6);
    next unless(($name eq 'HETATM')||($name eq 'ATOM  '));
    $array[$j][0] = substr($_,12,2);   # atom name, first two characters
    $array[$j][1] = substr($_,31,8);   # x
    $array[$j][2] = substr($_,39,8);   # y
    $array[$j][3] = substr($_,47,8);   # z
    $j++;
}

$array[$j-4][0] = 'Ca';
my $num_of_atom=$j;

for ($j=0;$j<$num_of_atom;$j++)
{
    printf OUT "%4s%s%15.8f%15.8f%15.8f\n", $array[$j][0], ' ', $array[$j][1], $array[$j][2], $array[$j][3];
}
