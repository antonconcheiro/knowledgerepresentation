{t3;t2;t1}.

% - & & t1 t2 t3.
:- t1, t2, t3.

% | | & t1 t2 & t1 t3 & t2 t3.
:- not t1, not t1, not t2.
:- not t2, not t1, not t2.
:- not t1, not t3, not t2.
:- not t2, not t3, not t2.
:- not t1, not t1, not t3.
:- not t2, not t1, not t3.
:- not t1, not t3, not t3.
:- not t2, not t3, not t3.

% - | | & t1 - t2 & t1 t2 & - t2 t2.
:- t1, not t2.
:- t1, t2.

