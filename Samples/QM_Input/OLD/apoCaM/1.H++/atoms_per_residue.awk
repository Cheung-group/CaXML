#!/bin/awk -f

{
    Num[$5]+=1
}

END {
    for (i in Num)
        print i, Num[i]
}

