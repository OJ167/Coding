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

%OK... I have f(sigma). Now they say they plot  the stream function 
% for theta = pi/s. Thus, I have to multiply f by sin^2(pi/2).
% However, sin(pi/2) = 1. Thus, I only have to plot f as a function
% of sigma.


figure
hold on
box on

plot(sigma,f)
 
 
 %Define physical aspect ratio of figure
 %pbaspect([1 2 1])

%Set axis limits
 xlim([1, 6])
 ylim([-12,0])
 %zlim([-3, 3])
 
%Define axis labels
 xlabel('sigma')
 ylabel('psi')
 %zlabel('f')
    
 
