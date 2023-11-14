#!/usr/bin/perl -w

################################################################################
# Convert pdb to xyz
# Usage: perl pdb2xyz.pl pdbfile.pdb
# Output: New.xyz
# xyz format:
# Atom x y z
# %4s%1s%10.5f%10.5f%10.5f
# Modified by P. Zhang, 11/13/2023
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
    $array[$j][1] = substr($_,17,3);   # residue name
    $array[$j][2] = substr($_,31,8);   # x
    $array[$j][3] = substr($_,39,8);   # y
    $array[$j][4] = substr($_,47,8);   # z
    $array[$j][4] = substr($_,47,8);   # z

    # HD HG HE --> H
    #if (($array[$j][0] eq 'HG') or ($array[$j][0] eq 'HD')) {
    if ($array[$j][0] =~ m/^H/) {
        $array[$j][0] = ' H';
    }

    if (($array[$j][1] eq ' CA') or ($array[$j][1] eq 'CAL')) {
        $array[$j][0] = 'Ca';
    }

    $j++;
}

my $num_of_atom=$j;
printf OUT "%d\n\n", $num_of_atom;

for ($j=0;$j<$num_of_atom;$j++)
{
    printf OUT "%4s%s%15.8f%15.8f%15.8f\n", $array[$j][0], ' ', $array[$j][2], $array[$j][3], $array[$j][4];
}
