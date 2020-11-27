# *identic*

The	 identic program	 will	 traverse	 the	 directories	 and	 look	 for	 files	 or	 directories that are duplicates of	each	other (i.e.	identical).	The	full	pathnames	of	duplicates	will	be	printed	as	output	(a new	line should	be	printed	between	the	sets	of	duplicates).

## Usage

```
identic [-f | -d ] [-i] [-c] [-n] [-s] [<dir1> < dir2> ..]
```


| Option | Definition|
| :---------: | --------------------|
|**[-f \| -d]**| -f	means	look	for	identical files,	-d	means	look	for	identical directories.	The	default	is	identical files.	|
|**-c** | Identical will	mean	the	contents	are	exactly	the	same	(note	that	the	names	can	be	different). |
| **-n**|  Identical	 will	mean	the	directory/file	names are	exactly	the	same	(note	that	the	contents can	be	different).|
| **-cn**| Identical	 will	mean	both the	contents	and	the	directory/file names	are	exactly	the	same.|
| **[\<dir1\> \<dir2\> ..]**| The	list	of	directories	to	traverse	(note	that	the	directories	will	be	traversed	recursively,	 i.e.	directories	and	their	subdirectories	and	their	subdirectories	etc.	etc.).	 The default is	current	directory.	 |
| **-s**| The	list	of	directories	to	traverse	(note	that	the	directories	will	be	traversed	recursively,	 i.e.	directories	and	their	subdirectories	and	their	subdirectories	etc.	etc.).	 The	default is	current	directory.	|