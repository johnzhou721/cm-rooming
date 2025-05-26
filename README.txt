Arranger 1.1.2
--------------

This is an Excel-based app for arranging rooms for field trips. Small rooms only — super slow + exponential growth for time complexity. Putting 30 people in rooms of 10 requires 20 seconds. Due to my contest math coach using a different format for rooming sheets (I was excited to see it but then was kinda unhappy to find it is not in my format), a converter to their format in VBA is written ("Word document converter").

Read manual/Manual.pdf for all documentation.
In manual/ are files referenced in the manual. manual/manual-source is source code of the manual, in which you should compile the arranger-doc.tex file with pdflatex.
Scripts required to be hooked up to the Excel sheet set up are in app-scripts/.
The VBA code for the Word document converter is in word-converter/.

Development Time: 9 weeks already excluding "breaks". 1 more week for documentation.


MISCELLANOUS

Contact
-------
John Zhou
Xinyuan.Z1@student.fortbendisd.com (FBISD, preferred, internal only)
john-xyz@outlook.com (Personal)
Email only, not phone
I am only a middle schooler.

All code and documentation copyright Xinyuan Zhou (c) 2024. All rights reserved. Permission granted to reproduce the *output* of this program in original/modified form without any restrictions.

To make sure you have all the files, here's the directory structure of this distribution:

Arranger-x.y.z.zip
├── README.txt
├── app-scripts
│   ├── Change-Room-Name.txt
│   ├── Highlight-Multiple.txt
│   ├── Main.txt
│   └── Move-Students.txt
├── manual
│   ├── Auto-Setup-Script.txt
│   ├── Manual.pdf
│   └── manual-source
│       ├── arranger-doc.tex
│       └── pic.png
└── word-converter
    └── WordDoc-convert.txt
