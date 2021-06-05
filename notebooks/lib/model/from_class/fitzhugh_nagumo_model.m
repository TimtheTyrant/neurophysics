% Fitzhugh-Nagumo model
% Timothy Tyree

function [ dy ] = Fitzhugh_Nagumo_Model(t, y, I_in)
% Fitzhugh_Nagumo_Model(t, y, I_in) compute the differential equations the Fitzhugh_Nagumo_Model.
%   Function returns the time differential of variables V, m, n and h.

%% Constent Parameters
I = 3 ; 
b = 1/2 ; 
%characteristic rate of the slow variable
phi = 0.01; % prefactor of n's rate equation in HHModel.m

%% define interaction functions

f  = @(V) (V-V.^3./3);
F1 = @(V,W) f(V) - W + I ;
F2 = @(V,W) phi.*(V-b.*W);


%% Set the variables for previous time step
V = y(1);
W = y(2);


dV = F1(V,W);
dW = F2(V,W);

dy = [dV dW]';

end

