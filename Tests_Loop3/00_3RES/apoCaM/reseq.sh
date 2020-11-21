#!/bin/bash

for i in {1..10}; do
    /bin/cp loop_3.model_$i.pdb tem.pdb
    ./reseq.pl
    /bin/mv New.pdb toPiotr/loop_3.model_$i.pdb
    rm -f tem.pdb
done
