%Input your coordinatematrix and your distancematrix as formatted by
%distance from coordinate to right of equals sign
%Concatenates atom number, x,y,z coordinate, and euclidean distance (5
%columns for each atom) 

datmatrix=datmatrix; %Coordinates
output=output; %Distance





Lc=length(datmatrix(1,:));
Rc=length(output(1,:));

commas = horzcat(datmatrix,output);
Imatrix=commas;


%Get rid of redundant atom numbers 
for c=Lc+1:Lc+(Rc-1)/2
    Imatrix=horzcat(Imatrix(:,1:(c-1)),Imatrix(:,(c+1):end));
end
commas = Imatrix;


%Reaarange columns
for c=5:5:Lc+(Rc-1)/2
    commas = horzcat(commas(:,1:(c-1)),Imatrix(:,(Lc + c/5)),commas(:,c:(Lc-1+c/5)),Imatrix(:,(Lc+1+c/5):end));
end
output1 = commas(:,1:end-1);
O = array2table(output1);
%writetable(O,'/home/nate/Desktop/PointDistance.txt')