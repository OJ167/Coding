clear
close all

% Defince sigma
m=1000;
sigmamin = 0.01;
sigmamax = 1.01;
%sigmamax = 4;
sigma = linspace(sigmamin,sigmamax,m);
sigmasquare = sigma.^2;

% Define polar coordinate theta and specify how many values to creat
p = pi;
n = 200;
theta = linspace(0,p,n);
sintheta = sin(theta);
costheta =cos(theta);
stsq = sintheta.^2;

%Calculate the pre-factors of Eq. (2.9) in Scase & Terry
Fac1a = 3 * sigmasquare; 
Fac1b =(1-sigmasquare);
Fac1c = (1/4) * (Fac1a .* Fac1b);

Fac2a = sigma.^3;
Fac2b = -1*(Fac2a - 1);
Fac2c = (1/2)*Fac2b;
Fac2d = Fac2c./sigma;


% Multiply the prefactor with each of the values in theta vector

for i = 1:n
   for j = 1:m 
             %Psi(i,j)= i*j;
          if sigma(j) <= 1
           Psi(i,j)= Fac1c(j)*stsq(i);
           %Psi(i,j)= i;
         else
           Psi(i,j)= Fac2d(j)*stsq(i);
           % Psi(i,j)= 0.1;
         end

   end    
end


   %for i=1:n  
   %      if sigma(i) <= 1
   %        Psi(i,:)= Fac1c.*stsq(i);
   %      else
   %        Psi(i,:)= Fac2d.*stsq(i);
   %      end
   %end       

    

%Calculate the x and y coordinate for each cell
for j = 1:m
   for i = 1:n
     x(i,j) = sintheta(i)*sigma(j);
     y(i,j) = costheta(i)*sigma(j);  
   end    
end


%surf(x,y,Psi)
%levels =  -7:0.5:10;
contour(x,y,Psi)
xlim([0, 4])
ylim([-2,2])
zlim([-3, 3])

  xlabel('x')
  ylabel('y')
  zlabel('Psi')
    
 %fprintf('Happy Birthday\n');

