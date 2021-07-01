#!/usr/bin/perl
# this program reads in cluster.dat and equil.pdb
# and generate outputs of coordiates for the transition states in the cluster 
if (@ARGV < 3){die "usage: a.out cluster number crdfile"; }

$clusterfile = shift @ARGV;
$Nnum = shift @ARGV;
$ensfile = shift @ARGV;
$ATOM=shift @ARGV;

open (INCLUSTER,$clusterfile) or die "cant open $clusterfile \n";
open (INCRD,$ensfile) or die "cant open $ensfile \n";
open (OUTCRD,">./cluster.pdb") or die "cant open cluster \n";

use POSIX;
$readline=$ATOM+1;
print "$readline lines per frame.\n";

print OUTCRD "cluster$Nnum\n";
while (<INCLUSTER>)
{
    chomp;
	@list= split(" ", $_); 
    push @number,  @list;
} 

@sortednumber = sort numerically @number;

$count=0;
while (<INCRD>)
{
    $count++;
}

close INCRD;

$Ntot=$count/$readline;
print "ens TOT $Ntot\n";


open (INCRD, $ensfile) or die "cant open $ensfile \n";

$sort=0;
for($i=0;$i<$Ntot;$i++) {
    @coor=();
    for($k=0;$k<$readline;$k++) {
        $_=<INCRD>;
        chomp;
        push @coor, $_;
    }

	if ($i eq $sortednumber[$sort])	
	{
        for ($l=1;$l<$readline;$l++)
        {
            print OUTCRD $coor[$l-1];
            printf(OUTCRD "\n");
        }
	    $sort++;
	}
} 

sub numerically
{
    $a <=> $b;
}
