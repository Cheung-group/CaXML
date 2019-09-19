 % normalize according to max in each column.

 s=load("vectors.dat");
 norms = s ./ max(s);
 dlmwrite('filename.txt',norms);
