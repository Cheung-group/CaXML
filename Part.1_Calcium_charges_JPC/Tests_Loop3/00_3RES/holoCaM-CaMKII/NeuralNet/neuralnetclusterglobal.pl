#!/usr/bin/perl
# Guo and Thirumalai F+D (2)p377-391,  1997. 
# input file is a file of Q.

#use strict; 
#use warnings;
#use diagnostics;

if(@ARGV < 1){die "usage: neuralnetclusterglobal.pl datafile"; }
my $datafile = shift @ARGV;

unless(open(OUTFILE, ">./neuralcluster.dat")){
    die("cant open output file\n");
}

unless(open(OUTFILE2, ">./cluster.dat")){
    die("cant open output file\n");
}

my $CUTOFF = 1.0;
my $Nk = 1;         #number of cluster. determined by phase 1
my @Nknum=();       #dynamic array, will be updated often
my @Ck=();          #dynamic array, will be updated often
my @Ckold=();       #dynamic array will be updated often
my %cluster = ();   #dynamic hash will be updated often
my $count = 0;
my $Ntot = 0;       #total number of TSE
my $Niteration = 1000;
my $TOL = 0.01;     #check whether it converges
my $MAXCONTACT = 45;#number of features 
my @vector;
my $n;

use POSIX;

#get data
& read_vectors();

#neural net
& phase_one();

#reproduce data
& read_vectors();

& phase_two();

& print_out();


sub phase_one 
{
##################################################
# Phase 1:  Learning phase.
# compute distance, assign clusters. use hash of hash for
# structured data
# find max cluster number Nk 
#################################################

    print "Phase 1 clustering\n\n";
	print OUTFILE "Learning phase\n";
    $Nk=0;
    my $num=0;
    my $totconf=0;
    my $dist=0;
    my $i=0;
    my $j=0;
    my $d=0;

    for($i=0;$i<$Ntot;$i++)
    {
	    if(defined $vector[$i]) 
        {
	        #dont forget, i itself should be included in the cluster.
	        $cluster{$Nk}{$num}=$i; 
	        $num++;

	        for($j=$i+1;$j<$Ntot;$j++)
	        {
		        if(defined $vector[$j])
			    { 
                    #print "good! vector $j is defined.\n";
			        #Euclidean distance
			        $dist=0;
			        for($d=0;$d<$MAXCONTACT;$d++)
			        {
		  	            $dist+=($vector[$j][$d]-$vector[$i][$d])*($vector[$j][$d]-$vector[$i][$d]);
                    }

			        $dist=sqrt($dist);
			        print "$i, $j, $dist, $CUTOFF\n";
			        if ($dist<$CUTOFF)
				    {
				        #add j to cluster i
			  	        #print "$i, $j, $dist, $CUTOFF\n";
				        $cluster{$Nk}{$num}=$j; 
				        #print "$Nk, $num, $cluster{$Nk}{$num}\n";
				        $num++;
				        #remove j from Q
				        undef($vector[$j]); 
				    }

	 		    } #end of if	
            } #end of j

 	        #number of conformations in cluster Nk	
	        $Nknum[$Nk] = keys %{$cluster{$Nk}};	

	        #print to file which conformations are associated with cluster Nk
            print OUTFILE "\n\nlearning: cluster $Nk, total $Nknum[$Nk]\n";

	        foreach my $x (sort {$cluster{$Nk}{$a} cmp $cluster{$Nk}{$b} } keys %{$cluster{$Nk}})
	        {
	            print OUTFILE "$cluster{$Nk}{$x}\t"; 
	        }	

            print "$Nk, $Nknum[$Nk]\n";
	        $totconf+=$Nknum[$Nk];
	        $Nk++;
	        $num=0;
        } # end of if
    } # end of i

    print "totconf $totconf Ntot $Ntot\n";
    if($totconf!=$Ntot) {print "error: totconf $totconf != Ntot $Ntot\n"; exit;}
} #end of phase one


sub phase_two 
{
#################################################
###########   Phase 2 refining Ck[Nk]
##########    until numbers  will not vary
################################################
 
    my $n;
    my $d;
    my $tot;
    my $i;
    my $j;
    my $index;
    my $np;
    my @distsort;
    my $distmin = 1000;
    my $newj;
    my $err;
    my $x;


    print "\n\nPhase 2 refining	\n\n";
    print OUTFILE "\n\nPhase 2 refining	\n\n";
    for($n=0;$n<$Niteration;$n++)
    {
	    print OUTFILE "\n\n iteration $n\n";
	    print "\niteration $n\n";
	    $tot=0;
	    for($i=0;$i<$Nk;$i++)	
	    {
	        #pass Ck{vector} to Ckold{vector};
	        for($d=0;$d<$MAXCONTACT;$d++)
	        {
	            $Ckold[$i][$d]=$Ck[$i][$d];
	            $Ck[$i][$d]=0;
	        }

	        #print "iter $n cluster $i, check Nknum $Nknum[$i]\n";
	        #compute cluster centers
	        $tot+=$Nknum[$i];	
	        for($j=0;$j<$Nknum[$i]; $j++)	
	        {
	            for($d=0;$d<$MAXCONTACT;$d++)
	            {
	                $index=$cluster{$i}{$j};
	                $Ck[$i][$d]+= $vector[$index][$d];
	            }
	        }

            #mark	
	        for($d=0;$d<$MAXCONTACT;$d++)
	        { 
	            if($Nknum[$i]>0){
	                $Ck[$i][$d]=$Ck[$i][$d]/$Nknum[$i];
	                $np=$n-1;
                    print OUTFILE "Iter $np cluster $i, vector $d center $Ck[$i][$d] \n";}
	        }

	        if($d eq 0){$tot+=$Nknum[$i];}
	    } #end of i
        
	    print "Nktot=$tot\n";
	
	    # reassign, check distance to each center, 
	    %cluster=();
	    @distsort=();
	    @Nknum=();
        for ($i=0;$i<$Ntot;$i++)
        {
	        $distmin=1000;
	        for($j=0;$j<$Nk;$j++)
	        {
                #Euclidean distance
	            for($d=0;$d<$MAXCONTACT;$d++)
                { 
		            $distsort[$j]+=($vector[$i][$d]-$Ck[$j][$d])*($vector[$i][$d]-$Ck[$j][$d]);
                }
		        $distsort[$j]=sqrt($distsort[$j]);
	            #print "conf $i, center $j, dist $distsort[$j] \n";
                #
		        if ($distsort[$j] < $distmin)
		        {
		            $distmin=$distsort[$j];
		            $newj=$j;
		        }
	        } #end of j

		    #add i to cluster newj 
            print "new cluster $newj num $Nknum[$newj] conf $i\n\n";
            $cluster{$newj}{$Nknum[$newj]} = $i;
            $Nknum[$newj]++;
        } #end of i

	    print "Iter $n:\n";
	    for($j=0;$j<$Nk;$j++)	
        { 
            print OUTFILE "\n\nIter $n cluster $j, total $Nknum[$j]\n";
            print "Iter $n cluster $j, total $Nknum[$j]\n";
            foreach $x(sort {$cluster{$j}{$a} cmp $cluster{$j}{$b} } keys %{$cluster{$j}})
            {
                print OUTFILE "$cluster{$j}{$x}\t";
            }
        } #end of j                                                                         

	    # check converges;
	    $err=0;
	    $tot=0;
	    for($i=0;$i<$Nk;$i++)
	    {
	        if($Nknum[$i]>0)
	        {
	            $tot+=1;
	            for($d=0;$d<$MAXCONTACT;$d++)
	            {
	                $err+=($Ckold[$i][$d]-$Ck[$i][$d])*($Ckold[$i][$d]-$Ck[$i][$d]);
                }
	        }
	    }

	    $err=$err/$Nk;
	    $err = sqrt($err);
	    print "error of centers from previous iteration = $err. number of cluster Nk= first $Nk last $tot\n";
	    if($err<$TOL){
		    print "Neural Net converges at N=$n\n\n"; 
       		for($j=0;$j<$Nk;$j++){
        		print OUTFILE2 "$Nknum[$j]\n";
          		foreach $x (sort {$cluster{$j}{$a} cmp $cluster{$j}{$b} } keys %{$cluster{$j}}){	
        			print OUTFILE2 "$cluster{$j}{$x}\t";
         		}		
       		 	print OUTFILE2 "\n";
         	} #end of j

		    for($j=0;$j<$Nk;$j++)
		    {
	            print OUTFILE "Last Iter $n cluster $j, total $Nknum[$j]\n";
            }	
		    last;
		}
    } #end of Niteration
} #end of phase two


sub print_out
{
    my $i;
    my $d;
    my $j;
    my $index;

	print OUTFILE "\n\n last iteration $n:\n";
	for ($i=0;$i< $Nk ; $i++)
    {
        for($d=0;$d<$MAXCONTACT;$d++)
        {
		    $Ck[$i][$d]=0;
        }                                                                                                        
        #print "iter $n cluster $i, check Nknum $Nknum[$i]\n";
                                                                                                                              
        for ($j=0;$j< $Nknum[$i] ; $j++)
        {
            $index=$cluster{$i}{$j};
 	        for($d=0;$d<$MAXCONTACT;$d++)
            {
                $Ck[$i][$d]+= $vector[$index][$d];
            }
            #print "$j index $index $Ck[$i],$cluster{$i}{$j},$Q[$index]\n";
        }

	    for($d=0;$d<$MAXCONTACT;$d++)
	    {
	        if($Nknum[$i]>0)
            { 
                $Ck[$i][$d]=$Ck[$i][$d]/$Nknum[$i];
                print OUTFILE "Iter $n cluster $i center $Ck[$i][$d] count $Nknum[$i]\n";}
            }
        }
} #end of print out


sub read_vectors
{
    @vector=();
    use Data::Dumper; 

    open my $INDATA, '<', "$datafile" or die "$datafile: $!";
    my $count=0;
    while(<$INDATA>){
        chomp;
        push @vector, [split /\s+/];
        $count++;
    }
    #print Dumper(@vector), "\n\n"; 
    $Ntot=$count;
    print "DATA TOT $Ntot\n";
}
