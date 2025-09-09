Code to sort people into rooms for a field trip at school.  For internal use only, just trying to be transparent w/ my math teacher about what's in the scripts attached to the workbooks I share with her.

Some minimal docs is at man.pdf.

Another thing: To separate the rooms after a bunch of grouping is already done a greedy algorithm is used that is NOT optimal but still sorta works that picks the 4 (or any # of people / room) people that when taken apart from the people that doesn't have rooms yet, breaks the least amount of constraints and put them in the room. So please I'm just telling you this is NOT going to work very well.

Docs in man.pdf.

arranger-2.0.py contains a reimplementation of all the management in Python but the actual solving is done using Pyomo (tested with CBC and SCIP).  There is PROBABLY a few bugs since I later found out that putting optimzation programs onto school computers is not feasible (pun intended, not feasible because you can't install random exe files, not in the sense of you can't package it for distribution -- just get a CPython embeddable package and begin aggressively copying DLLs from Anaconda repositories and their licenses), so it's abandoned.  Nevertheless (see #2) I'd still like to get some better heuristics into the V1 program.
