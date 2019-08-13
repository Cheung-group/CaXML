%Put in output from AddDistancetoCoordinates.m with the oxygen coordinates of the water
%molecule in column 177-179 and the calcium coordinates in 172-174 as well
%as the two water hydrogens in 182-184 and 187-189 might not be worth the
%trouble as results indicate this hardly has an effect on model accuracy



PointDistancematrix = table2array(PointDistance);
for r = 1:72
    midline = PointDistancematrix(r,177:179)-PointDistancematrix(r,172:174);
    Tmidline = transpose(midline);
    Lmidline = vecnorm(Tmidline);
    Odistance = mtimes(midline,Tmidline)/Lmidline;
    H1distance = mtimes(PointDistancematrix(r,182:184)-PointDistancematrix(r,172:174),Tmidline)/Lmidline;
    H2distance = mtimes(PointDistancematrix(r,187:189)-PointDistancematrix(r,172:174),Tmidline)/Lmidline;
    if (H1distance>Odistance) && (H2distance>Odistance)
        orientationmatrix(r,:) = [PointDistancematrix(r,1:190) 1 PointDistancematrix(r,191)];
    else 
        orientationmatrix(r,:) = [PointDistancematrix(r,1:190) 0 PointDistancematrix(r,191)];
    end
end
waterfeature = array2table(orientationmatrix);
%writetable(waterfeature, '/home/nate/Desktop/waterfeature.txt')