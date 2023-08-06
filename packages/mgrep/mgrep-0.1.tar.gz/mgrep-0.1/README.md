# mgrep

Multiprocess grep (mgrep) is a python grep implementation that utilises all available CPU 
cores to grep multiple files concurrently. For multiple large files it can provide a
20-25x speed increase.


Example test with 300 files of 25MB each (approx 7.5GB total)

grep:
```
# test grep
$ time grep "test.*a" * > /tmp/temp1.txt
grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "test.*a" * >   103.02s user 2.05s system 99% cpu 1:45.51 total
# test mgrep
$ time mgrep "test.*a" * > /tmp/temp2.txt
mgrep "test.*a" * > /tmp/temp2.txt  25.59s user 4.84s system 725% cpu 4.195 total
# confirm output of grep vs mgrep is identical
$ diff /tmp/temp1.txt /tmp/temp2.txt; echo $?
0
```

tl;dr a job that took ~105 seconds with grep takes ~4 seconds with mgrep

The main purpose of this project is to make James Ponting stop bugging me about it.


## Options

mgrep supports a handful of options:

* `-i/--ignore-case` (default: false)
    Run a case insensitive match

* `-r/--recursive` (default: false)
   Search files recursively

* `-c/--color` (default: auto)
   Display matched substrings in color