%Input any sized matrix in the following format
%Atomicnumber,xcoordinate,ycoordinate,zcoordinate,...,charge
%The 4 columns for the calcium atom must begin at column
%137(137,138,139,140)
%%%%%%%%%%%%%%%%%%%Outputs are surpressed by default. Uncomment
%%%%%%%%%%%%%%%%%%%'writetables' for desired output.
Inputdata=dat;           %input matrix




datmatrix=Inputdata;
inputc=length(datmatrix(1,:));
outputr=length(datmatrix(:,1));
outputc=(inputc+1)/2;
output = zeros(outputr,(inputc+1)/2);

for c = 1:inputc
    for r = 1:outputr
        if c==inputc
            output(r,end)= datmatrix(r,c);
        elseif mod(c,4)==1
            output(r,c-2*(c-1)/4)=datmatrix(r,c);
        elseif mod(c,4)==2
            output(r,c-2*(c-2)/4)=sqrt(power(datmatrix(r,c)-datmatrix(r,138),2)+power(datmatrix(r,c+1)-datmatrix(r,139),2)+power(datmatrix(r,c+2)-datmatrix(r,140),2));
        end
    end
end
T=array2table(output);
%writetable(T,'distance.txt')

%Seperate data into positive charges and negative charges to develop two
%hopefully more powerful predictors based on if its positive or negative.
pospassword = 0;
negpassword = 0;
positives = zeros(1,outputc);
negatives = zeros(1,outputc);
for r = 1:outputr
    if (output(r,outputc)<0) && (negpassword == 0)
        negatives(1,:) = output(r,:);
        negpassword = 1;
    elseif output(r,outputc)<0
        negatives = [negatives;output(r,:)];
    elseif pospassword == 0
        positives(1,:) = output(r,:);
        pospassword = 1;
    else 
        positives = [positives;output(r,:)];
    end
end 
P = array2table(positives);
N = array2table(negatives);
%writetable(P,'positivedistance.txt');
%writetable(N,'negativedistance.txt');
%Further break data into charge from 1.5 to 2.5 e
reasonable = zeros(1,outputc);
reasonablepassword=0;
for l = 1:60
    if (positives(l,outputc)<2.5) && (positives(l,outputc)>1.5) && (reasonablepassword==0)
        reasonable (1,:) = positives(l,:);
        reasonablepassword=1;
    elseif (positives(l,outputc)>1.5 && positives(l,outputc)<2.5)
        reasonable = [reasonable;positives(l,:)];
    end
end
R = array2table(reasonable);
%writetable(R,'/home/nate/Desktop/reasonabledistance.txt');