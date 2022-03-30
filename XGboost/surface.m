a= load('out.dat');
x=a(:,1); y=a(:,2); z=a(:,3);
%plot3(x,y,z, 'o');

%axis([0 10 0 14 1.5 2.1]);

xi= unique(x)';yi=unique(y);zi=griddata(x,y,z,xi,yi);
surf(xi,yi,zi);
%axis([25.0 44.0 0 180]);

caxis([1 2]);
%colorbar;
%xlabel('Closeness centrality calcium','FontSize',16);
%ylabel('Betweenness centrality AA10','FontSize',16);

