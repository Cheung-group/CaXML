#!/bin/bash
# convert tga to jpg

for f in *.tga;
	do convert -quality 100 $f `basename $f .tga`.png;
done
