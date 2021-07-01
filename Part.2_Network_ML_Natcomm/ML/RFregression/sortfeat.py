#!/usr/bin/env python
# coding: utf-8

inputf = open("features.txt", 'r')
outputf = open("feature-s.txt", 'w+')
hist = dict()

for line in inputf:
    line = line.strip().split()
    key = line[0]
    val = float(line[1])
    if key in hist:
        hist[key] += val
    else:
        hist[key] = val

import operator
sorted_hist = sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
for ele in sorted_hist:
    for j in ele:
        outputf.write(str(j)+"\t")
    outputf.write("\n")

outputf.close()

