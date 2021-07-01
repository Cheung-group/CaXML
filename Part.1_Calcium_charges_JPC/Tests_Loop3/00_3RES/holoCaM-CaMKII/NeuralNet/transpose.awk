## awk script to transpose a matrix
## usage: awk -f transpose.awk filename

BEGIN {FS=" "}

{
for (i=1;i<=NF;i++)
{
 arr[NR,i]=$i;
 if(big <= NF)
  big=NF;
 }
}

END {
  for(i=1;i<=big;i++)
   {
#    for(j=1;j<=NR;j++)
     j=2;
    {
     printf("%s\t",arr[j,i]);
    }
    printf("\n");
   }
}
