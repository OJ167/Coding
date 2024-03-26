clear
close all

% Set Rossby number
Ro = 0.1;


% Defince sigma
m=1000;
sigmamin = 0.01;
sigmamax = 7.01;
sigma = linspace(sigmamin,sigmamax,m);
sigmasquare = sigma.^2;
sigmamin1 =sigma - 1;

% Calculate f(sigma)
Term_1 = -1*(1/2)* sigmasquare;
Fac_1 = (1/2)*1./sigma;
Arg = (sigma - 1)/Ro;
Term_2 =  sigma.*cos(Arg);
Term_3 = Ro * sin(Arg);
Brack = Term_2 - Term_3;
f = Term_1 + Fac_1 .* Brack;


% Now we have f(sigma). However, in order to plot is
% as in Fig. 3 of Scase and Terry we need to introduce
% angle theta relative to upward z axis and then 
% convert f and theta to cartesian coordinates. 

% Define polar coordinate theta and specify how many values to creat
p = pi;
n = 80;
theta = linspace(0,p,n);
sintheta = sin(theta);
costheta = cos(theta);
sinthetasquare = sintheta.^2;

%Calculate the z coordinate for each f
for j = 1:m          %Note: m = number of radial points
   for i = 1:n       %Note: n = number of angles
     z(i,j) = costheta(i)*sigma(j);
     r(i,j) = sintheta(i)* sigma(j);
     Psi(i,j) = f(j)*sinthetasquare(i);
   end    
end


%Calculate the z coordinate for each f. But calculate r via x and y
%for j = 1:m          %Note: m = number of radial points
%   for i = 1:n       %Note: n = number of angles
%     x(i,j) = sintheta(i)*sigma(j);
%     y(i,j) = costheta(i)*sigma(j);  
%     r2(i,j) = sqrt(x(i,j)^2 + y(i,j)^2);
%     F(i,j) = f(j);
%   end    
% end



%surf(r,z,Psi)
figure
contour(r,z,Psi,50,'k-')
pbaspect([1 2 1])

% Plot Psi but using the other way of calucatiing r, that is r2 above
%figure
%contour(r2,z,Psi)
%pbaspect([1 2 1])
% NOTE: Both Plots are the same, so I too plot out again


xlim([0, 4])
ylim([-4,4])
%zlim([-3, 3])

  xlabel('r')
  ylabel('z')
  zlabel('f')
    
 %fprintf('Happy Birthday\n');

