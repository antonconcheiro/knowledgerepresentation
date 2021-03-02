{rain;happy;workday;weekend}.

% > | rain - weekend - happy.
:- rain, happy.
:- not weekend, happy.

% = weekend - workday.
:- workday, weekend.
:- not weekend, not workday.

