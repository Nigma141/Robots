clear all; close all ;

syms x y z l1 l2 l3 t1 t2 t3

A=[x;y;z;1];

B=[cos(t1) -sin(t1) 0 0;
    sin(t1) cos(t1) 0 0;
    0 0 1 0;
    0 0 0 1];

C=[cos(t2) -sin(t2) 0 0;
    0 0 -1 0;
    sin(t2) cos(t2) 0 l1;
    0 0 0 1];

D=[cos(t3) -sin(t3) 0 l2;
    sin(t3) cos(t3) 0 0;
    0 0 1 0;
    0 0 0 1];
E=[l3;
    0;
    0;
    1];


S=D*E
R=simplify(inv(C)*inv(B)*A)



%%
syms xp yp l1 l2 t1 t2 
xp=l