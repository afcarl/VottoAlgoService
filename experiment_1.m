%% Experiment 1: 
% 
% Assumptions 
%  - the shop sells only one product of price p of which the raw price is r. 
%  - odds are fixed. 

% Variables:
% N:average daily no of customers
% N_app: average daily no of customers with the app.
% w: discount rate of winning (e.g 0.75)
% l: discount rate of losing  (e.g 0.90)
% P_w: probability of winning the bet
% P_l: probability of losing  the bet
% P_sp:probability of winning a special offer. 

%Notes: some basic requiremetns
%     p*w, p*l > r  (otherwise no profits are made) i.e   r/p < l < w < 1. 
%     expected daily profit is given by N*p
%     expected daily profit with the app is given by 
%N_app*(P_w*p*w + (1-P_w)