function [ dy ] = HHModel(t, y, I_in)
% HHModel(t, y, I_in) compute the differential equations the Hodgkin-Huxley model.
%   Function returns the time differential of variables V, m, n and h.
%
%
%   Example:
%
%   T = 150;
%   I_current = 7;
%   y_ini = [0  0.05  0.3  0.6];
%
%   [t, y] = ode45(@(t, y) HHModel(t, y, I_current), [0  T], y_ini);
% 
%   V = y(:,1);
%   m = y(:,2);
%   n = y(:,3);
%   h = y(:,4);
%   plot(t, V)

%% 
% Constent Parameters
c_m =   1.0;  % (muF/cm^2)
gL  =   0.3;  % (mS/cm^2)
gNa = 120.0;
gK  =  36.0;

%  Nernst reversal potentials (mV)
Vt  =  25;%mV at RT
nernst = @(ion_out,ion_in) Vt*log(ion_out/ion_in);
VNa =  nernst(369.4528,50);  %in units of millimolar
VK  =  nernst(18.3837,400);
VL  =  -2.176*Vt;

%% 
% Set the variables for previous time step
V = y(1);
m = y(2);
n = y(3);
h = y(4);

% Differential equations of HH models
am = 0.10*(V + 40)./(1 - exp( -(V + 40)./10));      bm = 4*exp( -(V + 65)./18);
an = 0.01*(V + 55)./(1 - exp( -(V + 55)./10));      bn = 0.125*exp( -(V + 65)./(0.8*Vt));%unrevised 80);
ah = 0.07*exp(-(V + 65)./20);                       bh = 1./( 1 + exp( -(V + 35)./10));

I_Na = (V - VNa); % Na current
I_K  = (V - VK);  % K current
I_L  = (V - VL);  % Leaky current

dV = (- gL.* I_L - gNa* m.^3* h.* I_Na - gK* n.^4.* I_K + I_in)./c_m;
dm = am.*(1-m) - bm.*m;
dn = an.*(1-n) - bn.*n;
dh = ah.*(1-h) - bh.*h;

dy = [dV dm dn dh]';

end

