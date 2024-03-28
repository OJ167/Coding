clear
close all

% Set Rossby number
  Ro = 0.1;

% Set number of sreamlines to plot in contour plot
% for inside and outside of Hill's vortex
  SLinside = 10;
  SLoutside = 54;

% In order to plot things as in Fig. 3 of Scase and Terry 
% we need to introduce angle theta relative to upward 
% z axis. 
% Define polar coordinate theta and specify how many values 
% to create. Number of angles is n.
p = pi;
n = 80;
theta = linspace(0,p,n);
sintheta = sin(theta);
costheta = cos(theta);
sinthetasquare = sintheta.^2;

%Calculate data for a circle of radius 1
 RadCirc = 1;
  for i = 1:n
    XCirc(i) = RadCirc * sintheta(i);
    YCirc(i) = RadCirc * costheta(i);
  end


%START - CALCULATE STREAMLINES FOR sigma LARGER THAN 1
% Defince sigma
m=1000;
    %Note: Changing value of m does not have (much) of an effect on
    %the streamline patterns, provided the value of m is large enough.
    %Try running it with very low values of m, say m=5, and then
    %increase values to something like m=1000 or m=10000.
    %
    %Note: Changing the values of sigmamin and sigmamax changes
    %the appearance of the plots a bit. What is probably the
    %most relevant thing affecting things is probably the difference
    %between sigmamax and sigmamin, and also the number of contour
    %lines plotted in the contour(....) command at bottom
sigmamin = 1.01;  
    %Note: It works with sigmamin can be set to values below
    %one. What one gets is streamlines extending around the circle
    % for vortex.
sigmamax = 6.01;
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


%Calculate the z coordinate for each f
for j = 1:m          %Note: m = number of radial points
   for i = 1:n       %Note: n = number of angles
     z(i,j) = costheta(i)*sigma(j);
     r(i,j) = sintheta(i)* sigma(j);
     Psi(i,j) = f(j)*sinthetasquare(i);
   end    
end
%End - CALCULATE STREAMLINES FOR sigma > 1



%START - CALCULATE STREAMLINES FOR sigma SMALLER THAN 1
% That is inside the Hills vortex. To do this I simply copied over
% the block from above for sigma larger than 1 and then I put a 
% capital I infront of all variables to indicate it is for the Inner 
% bit of the vortex.
%
% Note: I cannot get the streamline shape inside the vortex the same was
% as it looks in Fig. 3 of Scase & Terry. No idea why.... I cannot really
% have a mistake in the code since I get the outside field OK and I have
% only copied the block for outside field over and changed the variable
% names by putting an I in front of each one. So, the formula for 
% f(sigma) has remained unchanged.  Also note that
% I had the same qualitative difference in yesterday's version of the code
% Where I calculated all in one go from sigmamin = 0.01 to sigmamax.

% Defince sigma
Im=1000;
Isigmamin = 0.01;
Isigmamax = 1.00;
Isigma = linspace(Isigmamin,Isigmamax,Im);
Isigmasquare = Isigma.^2;
Isigmamin1 =Isigma - 1;

% Calculate f(sigma)
ITerm_1 = -1*(1/2)* Isigmasquare;
IFac_1 = (1/2)*1./Isigma;
IArg = (Isigma - 1)/Ro;
ITerm_2 =  Isigma.*cos(IArg);
ITerm_3 = Ro * sin(IArg);
IBrack = ITerm_2 - ITerm_3;
If = ITerm_1 + IFac_1 .* IBrack;


%Calculate the z coordinate for each f
for j = 1:Im          %Note: m = number of radial points
   for i = 1:n       %Note: n = number of angles
     Iz(i,j) = costheta(i)*Isigma(j);
     Ir(i,j) = sintheta(i)* Isigma(j);
     IPsi(i,j) = If(j)*sinthetasquare(i);
   end    
end
%End - CALCULATE STREAMLINES FOR sigma > 1


%surf(r,z,Psi)
figure
hold on
box on
%Plot circle of radius 1
 plot(XCirc, YCirc,'r-','linewidth',1);

%Plot Steeamlines for sigma LARGE than 1
 contour(r,z,Psi,SLoutside,'k-')
 
 %Plot Steeamlines for sigma SMALLER than 1
 contour(Ir,Iz,IPsi,SLinside,'b-')

 %Define physical aspect ratio of figure
 pbaspect([1 2 1])

%Set axis limits
 xlim([0, 4])
 ylim([-4,4])
 %zlim([-3, 3])
 
%Define axis labels
 xlabel('r')
 ylabel('z')
 zlabel('f')
    
 
