# cm-rooming

(Internal codename:  Arranger)

Code to sort people into rooms for a field trip at school.  For internal use only, there's an easter egg in version 1.  This is mostly archival, but if you find any useful subrountines feel free to copy under license.

Some minimal docs is at man.pdf.  It explains the algorithm / how we settled on this' final form.

Another thing: To separate the rooms after a bunch of grouping is already done a greedy algorithm is used that is NOT optimal but still sorta works that picks the 4 (or any # of people / room) people that when taken apart from the people that doesn't have rooms yet, breaks the least amount of constraints and put them in the room.  So manual adjustment is needed.

## Version 2 (Unused in production)

arranger-2.0.py contains a reimplementation of all the management in Python but the actual solving is done using Pyomo (tested with CBC and SCIP).  There is PROBABLY a few bugs since I later found out that putting optimzation programs onto school computers is not feasible (pun intended, not feasible because you can't install random exe files, not in the sense of you can't package it for distribution -- just get a CPython embeddable package and begin aggressively copying DLLs from Anaconda repositories and their licenses), so it's abandoned.  Nevertheless (see #2) I'd still like to get some better heuristics into the V1 program.
