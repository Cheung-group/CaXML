# !/bin/bash


dir=.

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 PDB_Directory Calcium_radius Perform_Minimization (Yes/No)"
    echo "Example: $0 Selected 1.7 Yes"
    exit
fi

PDB=$1
r_ca=$(printf "%.2f" $2)
min=$3

# Generate single point calculation for Gaussian.

declare -A Chg
Chg=( [loop1]=0 [loop2]=-2 [loop3]=0 [loop4]=-3)

declare -A Mul
Mul=( [loop1]=1 [loop2]=1 [loop3]=1 [loop4]=1)



cat > template.inp << EOF
%chk=NNN.chk
%nprocshared=20
%mem=10GB
%nosave
#b3lyp/svp scf=(tight,noincore,xqc) Test
#IOP(5/87=12) Density=Current Pop=(MK,readradii) iop(6/33=2) iop(6/42=6)

NNN

   CHG  MUL

Ca $r_ca



EOF


if [ $min == "Yes" ]; then
    outdir="$dir"/"Ca_$r_ca"/"MIN_INP"

    rm -rf $outdir
    mkdir -p  $outdir

    for i in $PDB/loop*.pdb; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 1 -d .`
        echo working on model $i

        # convert pdb to the correct format
        # output New.xyz
        rm -f New.xyz
        rm -f Min.xyz
        perl "$dir"/pdb2xyz.pl $PDB/${i}.pdb

        num=`cat New.xyz | wc -l`
        #obminimize -n 100 -sd -ff uff New.xyz | tail -n $num > Min.xyz
	#Update: Newer version of openbabel does not support obminimize...
	obabel New.xyz -O Min.xyz --minimize --steps 100 --sd --ff uff

        sed -i 1,2d Min.xyz
        # replace the xyz part in the inp file
        sed '10 r Min.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp $outdir


        rm -f out${i}.pdb
        rm -f New.xyz
        rm -f Min.xyz
        rm -f template.inp
    done

else
    outdir="$dir"/"Ca_$r_ca"/"MD_INP"
    rm -rf $outdir
    mkdir -p $outdir

    for i in $PDB/loop*.pdb; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 1 -d .`
        echo working on model $i

        # convert pdb to the correct format
        # output New.xyz
        rm -f New.xyz
        perl "$dir"/pdb2xyz.pl $PDB/${i}.pdb
        sed -i 1,2d New.xyz
        # replace the xyz part in the inp file
        sed '10 r New.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp $outdir

        rm -f out${i}.pdb
        rm -f New.xyz
        rm -f Min.xyz
        rm -f template.inp
    done
fi

