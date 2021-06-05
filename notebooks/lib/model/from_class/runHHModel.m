function [ t, y ] = runHHModel(T, y_ini, tt_I, I_in)
% runHHModel(...) simulates the Hodgkin-Huxley model for the time dependent 
%   current inputs using the Euler method. Final time T, initial values of 
%   the variables y_ini, time step of the input currents tt_I, and currents 
%   I_in. The output y returns the time steps t, and the time series of membrane 
%   potential (V), and three gating variables (m, n, h).
%
%
%   Example 1:
%  
%   T = 1000 ; % msec
%   y_ini = [0  0.05  0.3  0.6];
%   tt_I = 0:0.1:T;
%   I_in = 10 * rand(length(tt_I), 1);
%   
%   [t, y] = runHHModel(T, y_ini, tt_I, I_in);
% 
%   V = y(:,1);
%   m = y(:,2);
%   n = y(:,3);
%   h = y(:,4);
%   plot(t, V)


dt = 0.001;
t = 0:dt:T;
y = zeros(length(t), length(y_ini));

intI = interp1(tt_I, I_in, t);
y(1, :) = y_ini;

for i = 1:length(t)-1
    
    % The changes of y for next time step
    dydt = HHModel(t(i), y(i, :), intI(i))' ;
    
    % Euler method for solving the OEDs.
    y(i+1, :) = y(i ,:) + dydt * dt;
    
end

