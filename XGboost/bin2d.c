/*
**  This program is to histogram according to the first two columns and average the third column.
**  Input number of bin_x, bin_y, x_low, x_high, y_low, y_high, input_file,  number_of_frames. 
**  For example:
**  ./2d and input "50 50 0 10 0 10 DAT 10000".
**  By Pengzhi Zhang, 2021
*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>

long unsigned int count;

int main()
{
    int i,j;
    int bin1,bin2;
	FILE *fp;
	double tem1,tem2,tem3,width1,width2;
	double lowlim1,uplim1,lowlim2,uplim2;
	int NHIS1,NHIS2;
	long unsigned int NUM;
	char infile[30],outfile[30];
	scanf("%d%d%lf%lf%lf%lf%s%ld",&NHIS1,&NHIS2,&lowlim1,&uplim1,&lowlim2,&uplim2,infile,&NUM);
	
	double ave[NHIS1][NHIS2];
	double err[NHIS1][NHIS2];
	double pi,pj;
	long unsigned int cnt[NHIS1][NHIS2];
	

	if(!(fp=fopen(infile,"r")))
        {
                printf("Cannot open data file.\n");
                exit(1);
        }

	count=0;

	/* determine the steplength of the histogram */ 
	width1=(uplim1-lowlim1)/(double)NHIS1;
	width2=(uplim2-lowlim2)/(double)NHIS2;
	
	/* initialization */
	for(bin1=0;bin1<NHIS1;bin1++)
    {
	    for(bin2=0;bin2<NHIS2;bin2++)
	    {
		    cnt[bin1][bin2]=0;
		    ave[bin1][bin2]=0.0;
		    err[bin1][bin2]=0.0;
	    }
    }

	/* main function */
    while (!feof(fp))
	{	
		fscanf(fp,"%lf%lf%lf\n",&tem1,&tem2,&tem3);
		bin1=(int)floor((tem1-lowlim1)/width1);
		bin2=(int)floor((tem2-lowlim2)/width2);
		if(bin1<NHIS1 && bin2<NHIS2)
		{
			ave[bin1][bin2]=ave[bin1][bin2]+tem3;
			err[bin1][bin2]=err[bin1][bin2]+(tem3*tem3);
			cnt[bin1][bin2]+=1;
		}
		count++;
//		printf("count:%ld!\n",count);
	}
	
	if(count!=NUM) 
	{
		printf("Wrong counts: %ld!\n",count);
		exit(1);
	} 
	
	for(i=0;i<NHIS1;i++)
    {
		pi=lowlim1+(i+0.5)*width1;
        for(j=0;j<NHIS2;j++)
	    {
		    pj=lowlim2+(j+0.5)*width2;
		    if(cnt[i][j]>0)
		    {
			    ave[i][j]=ave[i][j]/cnt[i][j];
			    err[i][j]=sqrt(err[i][j]/cnt[i][j]-ave[i][j]*ave[i][j])/sqrt(1);
			    printf("%lf\t%lf\t%lf\t%lf\n",pi,pj,ave[i][j],err[i][j]);
		    }
            else
            {
                printf("%lf\t%lf\t%lf\t%lf\n",pi,pj,0,0);
            }
	    }
    }

	return 0;
}		
