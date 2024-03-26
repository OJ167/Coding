clear
close all

% Set Rossby number
Ro = 0.1;


% Defince sigma
m=100;
sigmamin = 0.0;
sigmamax = 4.0;
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
n = 40;
theta = linspace(0,p,n);
sintheta = sin(theta);
costheta =cos(theta);

%Calculate the z coordinate for each f
for j = 1:m          %Note: m = number of radial points
   for i = 1:n       %Note: n = number of angles
     z(i,j) = costheta(i)*sigma(j);
     r(i,j) = sigma(j);
     F(i,j) = f(j);
   end    
end


%Calculate the z coordinate for each f. But calculate r via x and y
%for j = 1:m          %Note: m = number of radial points
%   for i = 1:n       %Note: n = number of angles
%     z(i,j) = costheta(i)*sigma(j);
%     x(i,j) = sintheta(i)*sigma(j);
%     y(i,j) = costheta(i)*sigma(j);  
%     r(i,j) = sqrt(x(i,j)^2 + y(i,j)^2);
%     F(i,j) = f(j);
%   end    
% end

%Try to do things in cartesian coordinates
%for j = 1:m
%   for i = 1:n
%     x(i,j) = sintheta(i)*sigma(j);
%     y(i,j) = costheta(i)*sigma(j);  
%   end    
% end


surf(r,z,F)
%contour(r,z,F)


%xlim([0, 0.2])
%ylim([-2,2])
%zlim([-3, 3])

  xlabel('r')
  ylabel('z')
  zlabel('f')
    
 %fprintf('Happy Birthday\n');

