/*
**  This program is to histogram according to the first column and average the second column.
**  Input number of bins, low_end, high_end, input file and number of frames . For example:
**  ./1d and input "50 0 10 DAT 10000".
**  By Pengzhi Zhang, July 11th, 2013
*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>

long unsigned int count;

int main()
{
        int i;
        int bin;
	FILE *fp;
	double tem1,tem2,width;
	double lowlim,uplim;
	int NHIS;
	long unsigned int NUM;
	char infile[30],outfile[30];
//	printf("number_of_bins  lowlim  uplim  input_file number_frames:\n");
	scanf("%d%lf%lf%s%ld",&NHIS,&lowlim,&uplim,infile,&NUM);
	
	double ave[NHIS];
	double err[NHIS];
	double p[NHIS];
	long unsigned int cnt[NHIS];
	

	if(!(fp=fopen(infile,"r")))
        {
                printf("Cannot open data file.\n");
                exit(1);
        }

	count=0;

	/* determine the steplength of the histogram */ 
	width=(uplim-lowlim)/(double)NHIS;
//printf("width=%lf",width);
	
	/* initialization */
	for(bin=0;bin<NHIS;bin++)
	{
		cnt[bin]=0;
		ave[bin]=0.0;
		err[bin]=0.0;
	}

	/* main function */
        while (!feof(fp))
	{	
		fscanf(fp,"%lf%lf\n",&tem1,&tem2);
		bin=(int)floor((tem1-lowlim)/width);
		if(bin<NHIS)
		{
			ave[bin]=ave[bin]+tem2;
			err[bin]=err[bin]+(tem2*tem2);
			cnt[bin]+=1;
		}
		count++;
//		printf("count:%ld!\n",count);
	}
	
	if(count!=NUM) 
	{
		printf("Wrong counts: %ld!\n",count);
		exit(1);
	} 
	
	for(i=0;i<NHIS;i++)
	{
		p[i]=lowlim+(i+0.5)*width;
		if(cnt[i]!=0)
		{
			ave[i]=ave[i]/cnt[i];
			err[i]=sqrt(err[i]/cnt[i]-ave[i]*ave[i])/sqrt(1);
			printf("%lf\t%lf\t%lf\n",p[i],ave[i],err[i]);
		}
	}

	return 0;
}		
