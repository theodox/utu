# Utu
### Cuneiform flashcard app

This is repo contains the website code and the tools for a cuneiform flashcard app.  The app relies on [pyodide](https://pyodide.org/en/stable/) and is written in Python. The web UI uses [Bootstrap 5.3](https://getbootstrap.com/)


## Sources
The data for the sign list was compiled from several sources:

* the [Wikipedia sign list](https://en.wikipedia.org/wiki/List_of_cuneiform_signs)
* [Kateřina Šašková's list](https://home.zcu.cz/~ksaskova/) from the University of Pilsen
* _An Akkadian Handbook_ by Douglas Miller and Mark Shipp
* _Complete Babylonian_ by Martin Worthington

with some checking against the [EPSD](http://oracc.museum.upenn.edu/epsd2/sux).  It is however still and amateur effort, please report any issues using the [Github issues link](https://github.com/theodox/utu/issues).

## The database

The actual database containing the signs, syllabograms, and logograms is contained in the file `cuneiform.db`.  This is a python 3.9 `sqllite3` database, it should be accessible in python 3 -- at least, on Windows. It might work on other OS'es but has not been tried. If you want a copy of the original data, contact me.

The raw data that was used to assemble the database is in `sourcdata.tsv`, a tab-separate spreadsheet, in the tools folder.  Note that the database includes some improvements over the organization of the sheet (for example, the sheet does not include the subscripts for different logogram versions). On the other hand `sourcedata.tsv` includes a number of signs and compounds that are not used in the actual app.


## License
© 2023 Steve Theodore.  This project is shared under the MIT License (see LICENSE.txt)