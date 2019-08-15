%input matrix of any size with charges in last column
input = distanceforrealmodels;



%Script will seperate positive and negative values
orientationmatrix=input;
pospassword = 0;
negpassword = 0;
pospointdistance = zeros(1,length(orientationmatrix(1,:)));
negpointdistance = zeros(1,length(orientationmatrix(1,:)));

for r = 1:length(orientationmatrix(:,1))
    if (orientationmatrix(r,end)<0) && (negpassword == 0)
        negpointdistance(1,:) = orientationmatrix(r,:);
        negpassword = 1;
    elseif orientationmatrix(r,end)<0
        negpointdistance = [negpointdistance;orientationmatrix(r,:)];
    elseif pospassword == 0
        pospointdistance(1,:) = orientationmatrix(r,:);
        pospassword = 1;
    else 
        pospointdistance = [pospointdistance;orientationmatrix(r,:)];
    end
end 
P1 = array2table(pospointdistance);
N1 = array2table(negpointdistance);
%writetable(P1,'/home/nate/Desktop/pospointdistance.txt');
writetable(N1,'/home/nate/Desktop/negpointdistance.txt');
writetable(P1,'/home/nate/Desktop/poswaterfeature.txt');
%goodvalues = zeros(1,192);
%for r = 1:60
 %   if (pospointdistance(r,192)>2.5)
  %  else 
   %     goodvalues = [goodvalues;pospointdistance(r,:)];
    %end
%end
%Goodoutput = array2table(goodvalues);
%writetable(Goodoutput,'/home/nate/Desktop/MachineLearning/Data');
